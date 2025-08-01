import polars as pl
import polars.selectors as cs

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
        
        Gracefully handles null struct values using conditional logic to avoid
        schema mismatch issues that can occur with fill_null approaches.
        
        Returns:
            A Polars expression that extracts the specified field from the struct,
            returning null for records where the struct or field is missing.
        """
        polars_struct = self.struct.to_polars()

        # return pl.struct([polars_struct.struct.field(f'^{self.fields}.*$'), pl.lit(None)]).struct[0] # pl.when(polars_struct.is_null()).then(pl.lit(None)).otherwise()
        # return pl.coalesce(polars_struct.struct.field(f'^{self.fields}$'), pl.lit(1)) # pl.when(polars_struct.is_null()).then(pl.lit(None)).otherwise()
        # return pl.struct(polars_struct.struct.field(f'^{self.fields}$'), pl.lit(1)).struct[0] # pl.when(polars_struct.is_null()).then(pl.lit(None)).otherwise()
        # return pl.when(polars_struct.is_null()).then(pl.struct(___dummy=pl.lit(None))).otherwise(polars_struct.struct.field(self.fields))
        # return pl.when(polars_struct.is_null()).then(pl.struct(___dummy=pl.lit(None))).otherwise(polars_struct).struct.field(self.fields)
        # return polars_struct.struct.field(f'^{self.fields}$').unnest().first(strict=False)
        # return polars_struct.struct.unnest().field(f'^{self.fields}$').unnest().first(strict=False)
        # safe_struct = pl.struct(pl.lit(1).alias('___dummy'))
        # polars_struct.pipe
        # safe_struct = pl.when(polars_struct.is_null()).then(pl.struct([pl.lit(1).alias('___dummy')])).otherwise(polars_struct)
        # return pl.fold(pl.lit(None), lambda acc, x: x, [pl.lit(None), polars_struct.struct.field(f'^{self.fields}$')])
        # return pl.reduce(lambda a, b: b, [pl.lit(None), polars_struct.struct.field(f'^{self.fields}$')])
        return polars_struct.map_elements(lambda x: x.get(self.fields) if x is not None else None, skip_nulls=False)