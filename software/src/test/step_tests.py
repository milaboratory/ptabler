import unittest
import polars as pl
from polars.testing import assert_frame_equal

from ptabler.workflow import PWorkflow
from ptabler.steps import GlobalSettings, AddColumns, Filter, TableSpace
from ptabler.steps.add_columns import ColumnDefinition
from ptabler.expression import (
    ColumnReferenceExpression, ConstantValueExpression,
    PlusExpression, EqExpression, GtExpression, AndExpression,
    ToUpperExpression, StringJoinExpression
)
from ptabler.expression.window import CumsumExpression, RankExpression
from ptabler.expression.fuzzy import StringDistanceExpression, FuzzyStringFilterExpression
from ptabler.expression.conditional import WhenThenClause, WhenThenOtherwiseExpression

# Minimal global_settings for tests not relying on file I/O from a specific root_folder
global_settings = GlobalSettings(root_folder=".")


class StepTests(unittest.TestCase):

    def test_add_columns_arithmetic(self):
        """
        Tests AddColumns step with a simple arithmetic expression.
        Adds a column 'c_sum' = col("a") + col("b").
        """
        initial_df = pl.DataFrame({
            "id": [1, 2],
            "a": [10, 20],
            "b": [5, 7]
        }).lazy()
        initial_table_space: TableSpace = {"input_table": initial_df}

        add_col_step = AddColumns(
            table="input_table",
            columns=[
                ColumnDefinition(
                    name="c_sum",
                    expression=PlusExpression(
                        lhs=ColumnReferenceExpression(name="a"),
                        rhs=ColumnReferenceExpression(name="b")
                    )
                )
            ]
        )

        workflow = PWorkflow(workflow=[add_col_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        expected_df = pl.DataFrame({
            "id": [1, 2],
            "a": [10, 20],
            "b": [5, 7],
            "c_sum": [15, 27]
        })

        result_df = final_table_space["input_table"].collect()
        assert_frame_equal(result_df, expected_df, check_dtypes=True)

    def test_filter_with_compound_condition(self):
        """
        Tests Filter step with a compound condition: value > 75 AND category == "A".
        The filtered result is stored in a new table "filtered_output".
        """
        initial_df = pl.DataFrame({
            "id": [1, 2, 3, 4],
            "value": [100, 50, 120, 80],
            "category": ["A", "B", "A", "B"]
        }).lazy()
        initial_table_space: TableSpace = {"source_table": initial_df}

        filter_step = Filter(
            input_table="source_table",
            output_table="filtered_output",
            condition=AndExpression(operands=[
                GtExpression(
                    lhs=ColumnReferenceExpression(name="value"),
                    rhs=ConstantValueExpression(value=75)
                ),
                EqExpression(
                    lhs=ColumnReferenceExpression(name="category"),
                    rhs=ConstantValueExpression(value="A")
                )
            ])
        )

        workflow = PWorkflow(workflow=[filter_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        expected_df = pl.DataFrame({
            "id": [1, 3],
            "value": [100, 120],
            "category": ["A", "A"]
        })

        self.assertTrue("filtered_output" in final_table_space)
        result_df = final_table_space["filtered_output"].collect()
        assert_frame_equal(result_df, expected_df, check_dtypes=True)

        # Ensure original table is still present and unchanged if needed for other tests,
        # though Filter creates a new one.
        self.assertTrue("source_table" in final_table_space)
        original_df_collected = final_table_space["source_table"].collect()
        assert_frame_equal(original_df_collected, initial_df.collect())

    def test_add_columns_string_operations_sequential(self):
        """
        Tests sequential AddColumns steps with string operations:
        1. Add 'first_upper' = to_upper(col("first"))
        2. Add 'full_name' = str_join([col("first_upper"), const(" "), col("last")])
        """
        initial_df = pl.DataFrame({
            "id": [1, 2],
            "first": ["john", "jane"],
            "last": ["doe", "smith"]
        }).lazy()
        initial_table_space: TableSpace = {"names_table": initial_df}

        add_upper_step = AddColumns(
            table="names_table",
            columns=[
                ColumnDefinition(
                    name="first_upper",
                    expression=ToUpperExpression(
                        value=ColumnReferenceExpression(name="first")
                    )
                )
            ]
        )

        add_full_name_step = AddColumns(
            table="names_table",
            columns=[
                ColumnDefinition(
                    name="full_name",
                    expression=StringJoinExpression(
                        operands=[
                            ColumnReferenceExpression(name="first_upper"),
                            ConstantValueExpression(value=" "),
                            ColumnReferenceExpression(name="last")
                        ],
                        delimiter=""  # Polars concat_str uses this as separator
                    )
                )
            ]
        )

        workflow = PWorkflow(workflow=[add_upper_step, add_full_name_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        expected_df = pl.DataFrame({
            "id": [1, 2],
            "first": ["john", "jane"],
            "last": ["doe", "smith"],
            "first_upper": ["JOHN", "JANE"],
            "full_name": ["JOHN doe", "JANE smith"]
        })

        result_df = final_table_space["names_table"].collect()
        # Order of columns might differ, so select in expected order for comparison
        result_df = result_df.select(expected_df.columns)
        assert_frame_equal(result_df, expected_df, check_dtypes=True)

    def test_cumsum_expression(self):
        """
        Tests AddColumns step with a CumsumExpression.
        Calculates cumulative sum of 'value' partitioned by 'category' and ordered by 'order_col'.
        """
        initial_df = pl.DataFrame({
            "id": [1, 2, 3, 4, 5, 6],
            "category": ["A", "A", "B", "A", "B", "B"],
            "value": [10, 20, 5, 15, 10, 20],
            "order_col": [1, 2, 1, 3, 2, 3]  # Order within each category
        }).lazy()
        initial_table_space: TableSpace = {"data_table": initial_df}

        cumsum_step = AddColumns(
            table="data_table",
            columns=[
                ColumnDefinition(
                    name="value_cumsum",
                    expression=CumsumExpression(
                        value=ColumnReferenceExpression(name="value"),
                        partition_by=[
                            ColumnReferenceExpression(name="category")],
                        additional_order_by=[
                            ColumnReferenceExpression(name="order_col")],
                        descending=False
                    )
                )
            ]
        )

        workflow = PWorkflow(workflow=[cumsum_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        expected_df = pl.DataFrame({
            "id": [1, 2, 4, 3, 5, 6],
            "category": ["A", "A", "A", "B", "B", "B"],
            "value": [10, 20, 15, 5, 10, 20],
            "order_col": [1, 2, 3, 1, 2, 3],
            "value_cumsum": [10, 25, 45, 5, 15, 35]
        })

        result_df = final_table_space["data_table"].collect().sort(
            ["category", "order_col"])
        assert_frame_equal(result_df, expected_df, check_dtypes=True)

    def test_rank_expression(self):
        """
        Tests AddColumns step with a RankExpression.
        Ranks 'value' partitioned by 'category', ordered by 'value' (desc) and 'id' (asc).
        """
        initial_df = pl.DataFrame({
            "id": [1, 2, 3, 4, 5, 6],
            "category": ["A", "B", "A", "B", "A", "B"],
            "value": [100, 200, 150, 200, 100, 300]
        }).lazy()
        initial_table_space: TableSpace = {"data_table": initial_df}

        rank_step = AddColumns(
            table="data_table",
            columns=[
                ColumnDefinition(
                    name="value_rank_desc",
                    expression=RankExpression(
                        order_by=[
                            ColumnReferenceExpression(name="value"),
                            ColumnReferenceExpression(name="id")
                        ],
                        partition_by=[
                            ColumnReferenceExpression(name="category")],
                        descending=True
                    )
                )
            ]
        )

        workflow = PWorkflow(workflow=[rank_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        result_df_collected = final_table_space["data_table"].collect()

        result_df_sorted = result_df_collected.sort(
            ["category", "value", "id"], descending=[False, True, True])

        expected_df = pl.DataFrame({
            "id": [3, 5, 1, 6, 4, 2],
            "category": ["A", "A", "A", "B", "B", "B"],
            "value":    [150, 100, 100, 300, 200, 200],
            "value_rank_desc": [1, 2, 3, 1, 2, 3]
        }, schema_overrides={"value_rank_desc": pl.UInt32})
        expected_df = expected_df.select(
            result_df_sorted.columns)  # Ensure column order

        assert_frame_equal(result_df_sorted, expected_df, check_dtypes=True)

    def test_string_distance_expression(self):
        """
        Tests AddColumns with StringDistanceExpression for Levenshtein.
        """
        initial_df = pl.DataFrame({
            "id": [1, 2, 3],
            "s1": ["apple", "banana", "orange"],
            "s2": ["apply", "bandana", "apricot"]
        }).lazy()
        initial_table_space: TableSpace = {"strings_table": initial_df}

        add_dist_step = AddColumns(
            table="strings_table",
            columns=[
                ColumnDefinition(
                    name="lev_dist",
                    expression=StringDistanceExpression(
                        metric="levenshtein",
                        string1=ColumnReferenceExpression(name="s1"),
                        string2=ColumnReferenceExpression(name="s2"),
                        return_similarity=False
                    )
                )
            ]
        )

        workflow = PWorkflow(workflow=[add_dist_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        expected_df = pl.DataFrame({
            "id": [1, 2, 3],
            "s1": ["apple", "banana", "orange"],
            "s2": ["apply", "bandana", "apricot"],
            "lev_dist": [1, 1, 6],  # Exact values
        }, schema_overrides={"lev_dist": pl.UInt32})

        result_df = final_table_space["strings_table"].collect()
        result_df = result_df.select(expected_df.columns)
        assert_frame_equal(result_df, expected_df, check_dtypes=True)

    def test_fuzzy_string_filter_expression(self):
        """
        Tests Filter step with a FuzzyStringFilterExpression using Levenshtein distance.
        Filters names that are <= 2 Levenshtein distance from "Michael".
        """
        initial_df = pl.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "name": ["Michael", "Micheal", "Miguel", "Michelle", "Robert"]
        }).lazy()
        initial_table_space: TableSpace = {"names_to_filter": initial_df}

        # Levenshtein distances from "Michael":
        # "Michael": 0
        # "Micheal": 1 (ea swap)
        # "Miguel":  3
        # "Michelle": 3
        # "Robert": >2 (e.g., 5 or 6)

        fuzzy_filter_step = Filter(
            input_table="names_to_filter",
            output_table="filtered_names",
            condition=FuzzyStringFilterExpression(
                metric="levenshtein",
                value=ColumnReferenceExpression(name="name"),
                pattern=ConstantValueExpression(value="Michael"),
                bound=2  # Max distance of 2
            )
        )

        workflow = PWorkflow(workflow=[fuzzy_filter_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        expected_df = pl.DataFrame({
            "id": [1, 2],  # Robert, Miguel, Michelle should be filtered out
            "name": ["Michael", "Micheal"]
        })

        self.assertTrue("filtered_names" in final_table_space)
        result_df = final_table_space["filtered_names"].collect()
        result_df = result_df.sort("id")
        expected_df = expected_df.sort("id")

        assert_frame_equal(result_df, expected_df, check_dtypes=True)

    def test_add_columns_with_conditional_expression(self):
        """
        Tests AddColumns step with a WhenThenOtherwiseExpression.
        Categorizes a 'value' column into 'High', 'Medium', or 'Low'.
        """
        initial_df = pl.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "value": [200, 75, 30, 100, 50]
        }).lazy()
        initial_table_space: TableSpace = {"source_data": initial_df}

        conditional_step = AddColumns(
            table="source_data",
            columns=[
                ColumnDefinition(
                    name="category",
                    expression=WhenThenOtherwiseExpression(
                        conditions=[
                            WhenThenClause(
                                when=GtExpression(
                                    lhs=ColumnReferenceExpression(name="value"),
                                    rhs=ConstantValueExpression(value=100)
                                ),
                                then=ConstantValueExpression(value="High")
                            ),
                            WhenThenClause(
                                when=GtExpression(
                                    lhs=ColumnReferenceExpression(name="value"),
                                    rhs=ConstantValueExpression(value=50)
                                ),
                                then=ConstantValueExpression(value="Medium")
                            )
                        ],
                        otherwise=ConstantValueExpression(value="Low")
                    )
                )
            ]
        )

        workflow = PWorkflow(workflow=[conditional_step])
        final_table_space, _ = workflow.execute(
            global_settings=global_settings,
            lazy=True,
            initial_table_space=initial_table_space
        )

        expected_df = pl.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "value": [200, 75, 30, 100, 50],
            "category": ["High", "Medium", "Low", "Medium", "Low"]
            # value=200 -> High (>100)
            # value=75  -> Medium (>50)
            # value=30  -> Low (else)
            # value=100 -> Medium (>50, not >100)
            # value=50  -> Low (else, not >50)
        })

        result_df = final_table_space["source_data"].collect()
        # Ensure column order for comparison
        result_df = result_df.select(expected_df.columns)
        result_df = result_df.sort("id")
        expected_df = expected_df.sort("id")

        assert_frame_equal(result_df, expected_df, check_dtypes=True)


if __name__ == '__main__':
    unittest.main()
