import typing
import polars as pl

from .base import Expression

AnyExpression = Expression


class StringJoinExpression(Expression, tag='str_join'):
    """
    Represents a string join operation on an array of expressions.
    Corresponds to the StringJoinExpression in TypeScript definitions.
    """
    operands: list['AnyExpression']
    """An array of expressions whose string representations will be joined."""
    delimiter: typing.Optional[str] = None
    """An optional delimiter string to insert between joined elements."""

    def to_polars(self) -> pl.Expr:
        """Converts the expression to a Polars concat_str expression."""
        polars_operands = [op.to_polars() for op in self.operands]
        return pl.concat_str(polars_operands, separator=self.delimiter or "")


class ToUpperExpression(Expression, tag='to_upper'):
    """Converts a string expression to uppercase."""
    value: 'AnyExpression'
    """The string expression to operate on."""

    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().str.to_uppercase()


class ToLowerExpression(Expression, tag='to_lower'):
    """Converts a string expression to lowercase."""
    value: 'AnyExpression'
    """The string expression to operate on."""

    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().str.to_lowercase()


class StrLenExpression(Expression, tag='str_len'):
    """Calculates the character length of a string expression."""
    value: 'AnyExpression'
    """The string expression to operate on."""

    def to_polars(self) -> pl.Expr:
        # Using len_chars for character count as per common expectation.
        # Use .str.len_bytes() if byte length is needed.
        return self.value.to_polars().str.len_chars()


class SubstringExpression(Expression, tag='substring'):
    """
    Represents a substring extraction operation on an expression.
    Corresponds to the SubstringExpression in TypeScript definitions.
    Extracts a portion of the string value resulting from the 'value' expression.
    The substring starts at the 'start' index (0-based).
    - If 'length' is provided, it specifies the maximum length of the substring.
    - If 'end' is provided, it specifies the index *before* which the substring ends.
    - If neither 'length' nor 'end' is provided, the substring extends to the end of the string.
    - 'length' and 'end' are mutually exclusive.
    If the requested substring range extends beyond the actual string length,
    the extraction automatically stops at the end of the string (Polars default behavior).
    """
    value: 'AnyExpression'
    """The expression whose string value will be used."""
    start: int
    """The starting position (0-indexed)."""
    length: typing.Optional[int] = None
    """The length of the substring. Mutually exclusive with 'end'."""
    end: typing.Optional[int] = None
    """The end position of the substring (exclusive). Mutually exclusive with 'length'."""

    def to_polars(self) -> pl.Expr:
        """Converts the expression to a Polars str.slice expression."""
        if self.length is not None and self.end is not None:
            raise ValueError(
                "SubstringExpression cannot have both 'length' and 'end' defined.")

        slice_length: typing.Optional[int] = None
        if self.length is not None:
            if self.length < 0:
                raise ValueError(
                    "SubstringExpression 'length' cannot be negative.")
            slice_length = self.length
        elif self.end is not None:
            if self.end < self.start:
                raise ValueError(
                    f"SubstringExpression 'end' ({self.end}) cannot be less than 'start' ({self.start}).")
            slice_length = self.end - self.start

        polars_value = self.value.to_polars()

        return polars_value.str.slice(offset=self.start, length=slice_length)
