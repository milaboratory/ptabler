import polars as pl
import os
from typing import List, Optional, Dict, Mapping, Any 
import msgspec

from ptabler.common import toPolarsType, PType

from .base import GlobalSettings, PStep, TableSpace
from .util import normalize_path

class ColumnSchema(msgspec.Struct, frozen=True, omit_defaults=True):
    """Defines the schema for a single column, mirroring the TS definition."""
    column: str
    type: Optional[PType] = None
    null_value: Optional[str] = None # Specific string to be interpreted as null for this column

class ReadCsv(PStep, tag="read_csv"):
    """
    PStep to read data from a CSV file into the tablespace.
    Corresponds to the ReadCsvStep in the TypeScript definitions.
    """
    file: str  # Path to the CSV file
    name: str  # Name to assign to the loaded DataFrame in the tablespace

    delimiter: Optional[str] = None
    schema: Optional[List[ColumnSchema]] = None
    columns: Optional[List[str]] = None # List of column names to read

    def execute(self, table_space: TableSpace, global_settings: GlobalSettings) -> tuple[TableSpace, list[pl.LazyFrame]]:
        """
        Reads the CSV file according to the step's parameters and adds the
        resulting LazyFrame to the tablespace.
        """
        scan_kwargs: Dict[str, Any] = {}

        if self.delimiter is not None:
            scan_kwargs["separator"] = self.delimiter
        
        if self.columns is not None:
            scan_kwargs["columns"] = self.columns

        processed_dtypes: Optional[Mapping[str, pl.DataType]] = None
        processed_null_values: Optional[Mapping[str, str]] = None

        if self.schema:
            current_dtypes: Dict[str, pl.DataType] = {}
            current_null_values: Dict[str, str] = {}
            has_any_type_in_schema = False
            has_any_null_in_schema = False

            for col_spec in self.schema:
                if col_spec.type:
                    polars_type_obj = toPolarsType(col_spec.type)
                    current_dtypes[col_spec.column] = polars_type_obj
                    has_any_type_in_schema = True
                
                if col_spec.null_value is not None:
                    current_null_values[col_spec.column] = col_spec.null_value
                    has_any_null_in_schema = True
            
            if has_any_type_in_schema:
                processed_dtypes = current_dtypes
            if has_any_null_in_schema:
                processed_null_values = current_null_values

        if processed_dtypes:
            scan_kwargs["schema"] = processed_dtypes
        
        if processed_null_values:
            scan_kwargs["null_values"] = processed_null_values
        
        lazy_frame = pl.scan_csv(os.path.join(global_settings.root_folder, normalize_path(self.file)), **scan_kwargs)
        
        updated_table_space = table_space.copy()
        updated_table_space[self.name] = lazy_frame
        
        return updated_table_space, []

class BaseWriteLogic(PStep):
    """
    Abstract base class for PSteps that write tables to files.
    It handles common logic like table retrieval from tablespace and column selection.
    Concrete subclasses must implement the _do_sink method.
    """
    # These attributes are expected to be defined by subclasses that are msgspec.Structs
    # and PStep compliant.
    table: str
    file: str
    columns: Optional[List[str]]

    def _do_sink(self, selected_lf: pl.LazyFrame, output_path: str) -> pl.LazyFrame:
        """
        Performs the specific sink operation for the derived class.
        This method should prepare and return a Polars LazyFrame representing the sink plan.
        """
        pass

    def execute(self, table_space: TableSpace, global_settings: GlobalSettings) -> tuple[TableSpace, list[pl.LazyFrame]]:
        """
        Common execution logic for writing steps.
        Retrieves the table, selects columns if specified, and then calls _do_sink.
        The actual write operation occurs when the returned LazyFrame (representing 
        the sink status) is collected by the main execution engine.
        """
        if self.table not in table_space:
            raise ValueError(
                f"Table '{self.table}' not found in tablespace. "
                f"Available tables: {list(table_space.keys())}"
            )

        lf_to_write = table_space[self.table]

        selected_lf = lf_to_write
        if self.columns:
            selected_lf = lf_to_write.select(self.columns)
        
        sink_plan = self._do_sink(selected_lf, os.path.join(global_settings.root_folder, normalize_path(self.file)))

        # The tablespace itself is not modified by a write operation.
        # We return the original tablespace and the plan that includes the sink operation.
        return table_space, [sink_plan]

class WriteCsv(BaseWriteLogic, tag="write_csv"):
    """
    PStep to write a table from the tablespace to a CSV file.
    Corresponds to the WriteCsvStep in the TypeScript definitions.
    """
    # Fields for msgspec - these are also "known" to BaseWriteLogic via type hints
    table: str  # Name of the table in the tablespace to write
    file: str   # Path to the output CSV file

    columns: Optional[List[str]] = None  # Optional: List of column names to write
    delimiter: Optional[str] = None      # Optional: The delimiter character for the output CSV

    # execute method is inherited from BaseWriteLogic

    def _do_sink(self, selected_lf: pl.LazyFrame, output_path: str) -> pl.LazyFrame:
        """
        Prepares a Polars plan to write the selected LazyFrame to a CSV file.
        """
        sink_kwargs: Dict[str, Any] = {}
        if self.delimiter is not None:
            sink_kwargs["separator"] = self.delimiter
        
        # Polars' sink_csv method with lazy=True prepares a plan that includes writing the CSV.
        # It returns a DataFrame which, when collected, performs the write
        # and contains status information.
        return selected_lf.sink_csv(
            path=output_path,
            lazy=True, # Ensures a plan is returned
            **sink_kwargs
        )

class WriteJson(BaseWriteLogic, tag="write_json"):
    """
    PStep to write a table from the tablespace to a JSON Lines file.
    Uses Polars' sink_ndjson for lazy writing.
    (Corresponds to a hypothetical WriteJsonStep in TypeScript definitions).
    """
    # Fields for msgspec
    table: str  # Name of the table in the tablespace to write
    file: str   # Path to the output JSON file
    columns: Optional[List[str]] = None  # Optional: List of column names to write
    # maintain_order: bool = True # Example: if we wanted to expose sink_ndjson's maintain_order

    # execute method is inherited from BaseWriteLogic

    def _do_sink(self, selected_lf: pl.LazyFrame, output_path: str) -> pl.LazyFrame:
        """
        Prepares a Polars plan to write the selected LazyFrame to a JSON Lines file.
        """
        # sink_ndjson for LazyFrame streams to a newline delimited JSON file.
        # It implicitly returns a plan. Default maintain_order=True is used by Polars.
        # If other sink_ndjson parameters (like maintain_order) need to be configurable,
        # they should be added as fields to this class and passed to sink_ndjson.
        return selected_lf.sink_ndjson(
            path=output_path
            # maintain_order=self.maintain_order # If maintain_order field was added
            )
