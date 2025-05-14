import unittest
import polars as pl
from polars.testing import assert_frame_equal

from ptabler.workflow import PWorkflow
from ptabler.steps import GlobalSettings, Join, TableSpace
from ptabler.expression import ColumnReferenceExpression

# Minimal global_settings for tests
global_settings = GlobalSettings(root_folder=".")


class JoinStepTests(unittest.TestCase):

    def setUp(self):
        """Setup common data for join tests."""
        self.left_df = pl.DataFrame({
            "id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Charlie", "David"],
            "value_left": [10, 20, 30, 40]
        }).lazy()

        self.right_df = pl.DataFrame({
            "id": [1, 2, 3, 5],
            "city": ["New York", "London", "Paris", "Berlin"],
            "value_right": [100, 200, 300, 500]
        }).lazy()

        self.initial_table_space: TableSpace = {
            "left_table": self.left_df,
            "right_table": self.right_df
        }

    def _execute_join_workflow(self, join_step: Join) -> pl.DataFrame:
        """Helper to execute a workflow with a single join step."""
        workflow = PWorkflow(workflow=[join_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=self.initial_table_space.copy()
        )
        self.assertTrue("joined_output" in final_table_space)
        return final_table_space["joined_output"].collect()

    def test_inner_join(self):
        """Tests an inner join."""
        join_step = Join(
            left_table="left_table",
            right_table="right_table",
            output_table="joined_output",
            how="inner",
            left_on=["id"],
            right_on=["id"]
        )
        result_df = self._execute_join_workflow(join_step)

        expected_df = pl.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value_left": [10, 20, 30],
            "city": ["New York", "London", "Paris"],
            "value_right": [100, 200, 300]
        }).sort("id")
        # Ensure 'id_right' is not present (should be handled by explicit column selection now)
        self.assertNotIn("id_right", result_df.columns, "Column 'id_right' should not be present after join with explicit column selection.")

        assert_frame_equal(result_df.sort("id"), expected_df, check_dtypes=False)


    def test_left_join(self):
        """Tests a left join."""
        join_step = Join(
            left_table="left_table",
            right_table="right_table",
            output_table="joined_output",
            how="left",
            left_on=["id"],
            right_on=["id"],
            left_columns={"id": "id", "name": "name", "value_left": "value_left"},
            right_columns={"id": "id", "city": "city", "value_right": "value_right"}
        )
        result_df = self._execute_join_workflow(join_step)

        expected_df = pl.DataFrame({
            "id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Charlie", "David"],
            "value_left": [10, 20, 30, 40],
            "city": ["New York", "London", "Paris", None],
            "value_right": [100, 200, 300, None]
        }, schema_overrides={"value_right": pl.Int64}).sort("id")
        # Ensure 'id_right' is not present
        self.assertNotIn("id_right", result_df.columns, "Column 'id_right' should not be present after join with explicit column selection.")

        assert_frame_equal(result_df.sort("id"), expected_df, check_dtypes=False)


    def test_outer_join(self):
        """Tests an outer join."""
        join_step = Join(
            left_table="left_table",
            right_table="right_table",
            output_table="joined_output",
            how="outer",
            left_on=["id"],
            right_on=["id"],
            left_columns={"id": "id", "name": "name", "value_left": "value_left"},
            right_columns={"id": "id", "city": "city", "value_right": "value_right"}
        )
        result_df = self._execute_join_workflow(join_step)

        expected_df = pl.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", None],
            "value_left": [10, 20, 30, 40, None],
            "city": ["New York", "London", "Paris", None, "Berlin"],
            "value_right": [100, 200, 300, None, 500]
        }, schema_overrides={"value_left": pl.Int64, "value_right": pl.Int64}).sort("id")
        
        # Handle Polars' default behavior for outer joins where it creates 'id' and 'id_right'
        # when join keys (left_on, right_on) are named the same, even after left_columns/right_columns aliasing.
        if "id_right" in result_df.columns and "id" in result_df.columns:
            # Coalesce 'id' from left and 'id_right' from right into a single 'id' column
            result_df = result_df.with_columns(
                pl.coalesce(pl.col("id"), pl.col("id_right")).alias("id_coalesced")
            ).drop("id", "id_right").rename({"id_coalesced": "id"})
        elif "id_right" in result_df.columns and "id" not in result_df.columns:
            # This case might occur if the left 'id' column was somehow not selected or was named differently
            # prior to the join, and only 'id_right' came through.
            result_df = result_df.rename({"id_right": "id"})
        
        # After handling, 'id_right' should not be present, and 'id' should be the coalesced key.
        self.assertNotIn("id_right", result_df.columns, "Column 'id_right' should have been removed after coalescing.")
        self.assertIn("id", result_df.columns, "Column 'id' should be present as the coalesced key.")

        # Ensure columns are in the expected order for comparison and select only expected columns
        result_df_ordered = result_df.select(expected_df.columns)

        assert_frame_equal(result_df_ordered.sort("id"), expected_df, check_dtypes=False)

    def test_cross_join(self):
        """Tests a cross join."""
        # For cross join, let's use smaller DFs to keep the output manageable
        left_small_df = pl.DataFrame({"lk": ["L1", "L2"]}).lazy()
        right_small_df = pl.DataFrame({"rk": ["R1", "R2", "R3"]}).lazy()

        initial_cs_table_space: TableSpace = {
            "left_small": left_small_df,
            "right_small": right_small_df
        }

        join_step = Join(
            left_table="left_small",
            right_table="right_small",
            output_table="joined_output",
            how="cross",
            # No left_on or right_on for cross join
            left_columns={"lk": "lk"},
            right_columns={"rk": "rk"}
        )

        workflow = PWorkflow(workflow=[join_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_cs_table_space
        )
        self.assertTrue("joined_output" in final_table_space)
        result_df = final_table_space["joined_output"].collect()


        expected_df = pl.DataFrame({
            "lk": ["L1", "L1", "L1", "L2", "L2", "L2"],
            "rk": ["R1", "R2", "R3", "R1", "R2", "R3"],
        }).sort(["lk", "rk"])


        assert_frame_equal(result_df.sort(["lk", "rk"]), expected_df, check_dtypes=False)

    def test_join_with_different_key_names(self):
        """Tests a join where left_on and right_on have different column names."""
        # Original right_df is used, renaming is handled by right_columns
        # right_df_renamed_key = self.right_df.rename({"id": "key_right"}).lazy() 
        
        temp_initial_table_space: TableSpace = {
            "left_table": self.left_df,
            "right_table": self.right_df # Use original right_df
        }

        join_step = Join(
            left_table="left_table",
            right_table="right_table", # Use original right_df
            output_table="joined_output",
            how="inner",
            left_on=["id"], # This will be the name from left_columns
            right_on=["key_right"], # This will be the name from right_columns
            left_columns={"id": "id", "name": "name", "value_left": "value_left"},
            right_columns={"id": "key_right", "city": "city", "value_right": "value_right"}
        )
        
        workflow = PWorkflow(workflow=[join_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=temp_initial_table_space.copy()
        )
        self.assertTrue("joined_output" in final_table_space)
        result_df = final_table_space["joined_output"].collect()


        expected_df = pl.DataFrame({
            "id": [1, 2, 3], # Key column name comes from left_on
            "name": ["Alice", "Bob", "Charlie"],
            "value_left": [10, 20, 30],
            "city": ["New York", "London", "Paris"],
            "value_right": [100, 200, 300]
        }).sort("id")
        
        # Polars by default only keeps the left key column if names in left_on/right_on differ.
        # So, 'key_right' (the name used in right_on) should not be in result_df.
        self.assertNotIn("key_right", result_df.columns)
        self.assertIn("id", result_df.columns) # The key from left_on should be present

        assert_frame_equal(result_df.sort("id"), expected_df, check_dtypes=False)

    def test_error_missing_left_on_for_non_cross_join(self):
        """Tests that a ValueError is raised if left_on is missing for a non-cross join."""
        with self.assertRaisesRegex(ValueError, "Missing 'left_on' for 'inner' join."):
            join_step = Join(
                left_table="left_table",
                right_table="right_table",
                output_table="joined_output",
                how="inner",
                # left_on is missing
                right_on=["id"]
            )
            self._execute_join_workflow(join_step)
            
    def test_error_missing_right_on_for_non_cross_join(self):
        """Tests that a ValueError is raised if right_on is missing for a non-cross join."""
        with self.assertRaisesRegex(ValueError, "Missing 'right_on' for 'left' join."):
            join_step = Join(
                left_table="left_table",
                right_table="right_table",
                output_table="joined_output",
                how="left",
                left_on=["id"]
                # right_on is missing
            )
            self._execute_join_workflow(join_step)

    def test_error_left_table_not_found(self):
        """Tests error when left_table is not in tablespace."""
        with self.assertRaisesRegex(ValueError, "Left table 'nonexistent_left_table' not found in tablespace."):
            join_step = Join(
                left_table="nonexistent_left_table",
                right_table="right_table",
                output_table="joined_output",
                how="inner",
                left_on=["id"],
                right_on=["id"]
            )
            self._execute_join_workflow(join_step)

    def test_error_right_table_not_found(self):
        """Tests error when right_table is not in tablespace."""
        with self.assertRaisesRegex(ValueError, "Right table 'nonexistent_right_table' not found in tablespace."):
            join_step = Join(
                left_table="left_table",
                right_table="nonexistent_right_table",
                output_table="joined_output",
                how="inner",
                left_on=["id"],
                right_on=["id"]
            )
            self._execute_join_workflow(join_step)


if __name__ == '__main__':
    unittest.main()
