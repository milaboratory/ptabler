import polars as pl

from .base import Expression


class RankExpression(Expression, tag='rank', rename="camel"):
    """
    Represents a rank function applied over a dataset partition.
    Calculates the rank of each row within its partition based on the specified ordering.
    Corresponds to the RankExpression in TypeScript definitions.
    Uses Polars' dense rank method by default.
    """
    order_by: list[Expression]
    partition_by: list[Expression]
    descending: bool = False

    def to_polars(self) -> pl.Expr:
        """Converts the expression to a Polars rank window expression."""
        polars_partitions = [p.to_polars() for p in self.partition_by]
        polars_order_exprs = [ob.to_polars() for ob in self.order_by]

        if not polars_order_exprs:
            raise ValueError(
                "RankExpression requires at least one 'order_by' expression.")

        rank_expr = pl.struct(polars_order_exprs).rank(
            "ordinal", descending=self.descending)

        if polars_partitions:
            return rank_expr.over(polars_partitions)
        else:
            return rank_expr


class CumsumExpression(Expression, tag='cumsum', rename="camel"):
    """
    Represents a cumulative sum function applied over a dataset partition, respecting order.
    Calculates the cumulative sum of the 'value' expression within each partition,
    based on the specified ordering (value first, then additional_order_by).
    Corresponds to the CumsumExpression in TypeScript definitions.
    """
    value: Expression
    additional_order_by: list[Expression]
    partition_by: list[Expression]
    descending: bool = False

    def to_polars(self) -> pl.Expr:
        """Converts the expression to a Polars cumsum window expression."""
        polars_value = self.value.to_polars()
        polars_partitions = [p.to_polars() for p in self.partition_by]
        polars_additional_order = [ob.to_polars()
                                   for ob in self.additional_order_by]

        combined_order_exprs = [polars_value] + polars_additional_order

        descending_flags = [self.descending] * len(combined_order_exprs)

        sorted_value_expr = polars_value.sort_by(
            combined_order_exprs, descending=descending_flags)

        cumsum_after_sort_expr = sorted_value_expr.cum_sum()

        if polars_partitions:
            return cumsum_after_sort_expr.over(polars_partitions)
        else:
            return cumsum_after_sort_expr
