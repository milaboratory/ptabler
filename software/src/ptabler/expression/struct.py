import typing
import polars as pl

from .base import Expression

AnyExpression = Expression


class StructFieldExpression(Expression, tag='struct_field'):
    """
    Represents a struct field access operation for nested data structures.
    Extracts one or more fields from a struct expression, commonly used for JSON data.
    Corresponds to the StructFieldExpression in TypeScript definitions.
    Uses Polars' struct.field functionality for accessing nested fields.
    """
    struct: 'AnyExpression'
    """The struct expression to extract fields from."""
    fields: str
    """
    The field name to extract from the struct.
    Currently only supports single field extraction.
    """

    def to_polars(self) -> pl.Expr:
        """
        Converts the expression to a Polars struct.field expression.
        
        Returns:
            A Polars expression that extracts the specified field from the struct.
        """
        polars_struct = self.struct.to_polars()
        return polars_struct.struct.field(self.fields)