import polars as pl
import msgspec
from typing import List

from .base import GlobalSettings, PStep, TableSpace
from ..expression import AnyExpression


class ColumnDefinition(msgspec.Struct, frozen=True, rename="camel"):
    """
    Defines a new column to be added to a table.
    It specifies the name of the new column and the expression used to compute its values.
    """
    name: str
    expression: AnyExpression


class AddColumns(PStep, tag="add_columns"):
    """
    PStep to add one or more new columns to an existing table in the tablespace.

    This step retrieves a specified table (LazyFrame) from the tablespace,
    computes new columns based on the provided expressions, and updates the
    table in the tablespace with these new columns.
    Corresponds to the AddColumnsStep defined in the TypeScript type definitions.
    """
    table: str
    columns: List[ColumnDefinition]

    def execute(self, table_space: TableSpace, global_settings: GlobalSettings) -> tuple[TableSpace, list[pl.LazyFrame]]:
        """
        Executes the add_columns step.

        Args:
            table_space: The current tablespace containing named LazyFrames.
            global_settings: Global settings for the workflow.

        Returns:
            A tuple containing the updated tablespace and an empty list (as this is not a sink operation).
        
        Raises:
            ValueError: If the specified table is not found in the tablespace.
        """
        if self.table not in table_space:
            raise ValueError(
                f"Table '{self.table}' not found in tablespace. "
                f"Available tables: {list(table_space.keys())}"
            )

        lf = table_space[self.table]

        polars_expressions_to_add = []
        for col_def in self.columns:
            # Each Expression object has a to_polars() method that converts it
            # to a Polars expression. It's then aliased to the new column name.
            polars_expr = col_def.expression.to_polars().alias(col_def.name)
            polars_expressions_to_add.append(polars_expr)

        if polars_expressions_to_add:
            lf = lf.with_columns(polars_expressions_to_add)

        # Update the tablespace with the modified LazyFrame
        updated_table_space = table_space.copy()
        updated_table_space[self.table] = lf
        
        return updated_table_space, []
