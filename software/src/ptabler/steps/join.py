import polars as pl
from typing import Literal, Optional

from .base import GlobalSettings, PStep, TableSpace


class Join(PStep, tag="join"):
    """
    PStep to join two tables from the tablespace.

    Corresponds to the JoinStep or CrossJoinStep defined in the TypeScript type definitions.
    """
    left_table: str
    right_table: str
    output_table: str
    how: Literal["inner", "left", "right", "outer", "cross"]
    # Optional, as not needed for cross join
    left_on: Optional[list[str]] = None
    # Optional, as not needed for cross join
    right_on: Optional[list[str]] = None
    # Optional fields to select and rename columns
    left_columns: Optional[dict[str, str]] = None
    right_columns: Optional[dict[str, str]] = None

    def execute(self, table_space: TableSpace, global_settings: GlobalSettings) -> tuple[TableSpace, list[pl.LazyFrame]]:
        """
        Executes the join step.

        Args:
            table_space: The current tablespace containing named LazyFrames.
            global_settings: Global settings for the workflow.

        Returns:
            A tuple containing the updated tablespace and an empty list (as this is not a sink operation).

        Raises:
            ValueError: If input tables are not found or if join keys are missing for non-cross joins.
        """
        if self.left_table not in table_space:
            raise ValueError(
                f"Left table '{self.left_table}' not found in tablespace. "
                f"Available tables: {list(table_space.keys())}"
            )
        if self.right_table not in table_space:
            raise ValueError(
                f"Right table '{self.right_table}' not found in tablespace. "
                f"Available tables: {list(table_space.keys())}"
            )

        left_lf = table_space[self.left_table]
        right_lf = table_space[self.right_table]

        if self.left_columns:
            left_lf = left_lf.select(
                [pl.col(original_name).alias(new_name) for original_name, new_name in self.left_columns.items()]
            )

        if self.right_columns:
            right_lf = right_lf.select(
                [pl.col(original_name).alias(new_name) for original_name, new_name in self.right_columns.items()]
            )

        joined_lf: pl.LazyFrame

        if self.how == "cross":
            joined_lf = left_lf.join(right_lf, how="cross")
        else:
            if not self.left_on:
                raise ValueError(f"Missing 'left_on' for '{self.how}' join.")
            if not self.right_on:
                raise ValueError(f"Missing 'right_on' for '{self.how}' join.")

            joined_lf = left_lf.join(
                right_lf,
                left_on=self.left_on,
                right_on=self.right_on,
                how=self.how
            )

        updated_table_space = table_space.copy()
        updated_table_space[self.output_table] = joined_lf

        return updated_table_space, []
