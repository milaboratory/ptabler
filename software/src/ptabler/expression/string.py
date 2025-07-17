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


class SubstringExpression(Expression, tag="substring"):
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
    'start', 'length', and 'end' can be either literal integers or expression objects.
    """

    value: "AnyExpression"
    """The expression whose string value will be used."""
    start: typing.Union[int, "AnyExpression"]
    """The starting position (0-indexed), as a literal or an expression."""
    length: typing.Optional[typing.Union[int, "AnyExpression"]] = None
    """The length of the substring. Mutually exclusive with 'end'."""
    end: typing.Optional[typing.Union[int, "AnyExpression"]] = None
    """The end position of the substring (exclusive). Mutually exclusive with 'length'."""

    def to_polars(self) -> pl.Expr:
        """Converts the expression to a Polars str.slice expression."""
        if self.length is not None and self.end is not None:
            raise ValueError("SubstringExpression cannot have both 'length' and 'end' defined.")

        polars_value = self.value.to_polars()

        def to_polars_expr(val):
            if isinstance(val, Expression):
                return val.to_polars()
            elif isinstance(val, int):
                return pl.lit(val)
            else:
                raise TypeError(f"Unsupported type for substring parameter: {type(val)}")

        polars_start = to_polars_expr(self.start)

        slice_length: typing.Optional[pl.Expr] = None
        if self.length is not None:
            if isinstance(self.length, int) and self.length < 0:
                raise ValueError("SubstringExpression 'length' cannot be negative.")
            slice_length = to_polars_expr(self.length)
        elif self.end is not None:
            polars_end = to_polars_expr(self.end)
            slice_length = polars_end - polars_start

        return polars_value.str.slice(offset=polars_start, length=slice_length)


class StringReplaceExpression(Expression, tag="str_replace"):
    """
    Represents a string replacement operation.
    Corresponds to the StringReplaceExpression in TypeScript definitions.
    Replaces occurrences of a pattern (regex or literal) in a string expression
    with a replacement string.
    """
    value: 'AnyExpression'
    """The input string expression to operate on."""
    pattern: typing.Union['AnyExpression', str]
    """The pattern (regex or literal string) to search for."""
    replacement: typing.Union['AnyExpression', str]
    """The replacement string. Can use $n or ${name} for captured groups if pattern is a regex."""
    replace_all: typing.Optional[bool] = False
    """If true, replace all occurrences. If false (default), replace only the first."""
    literal: typing.Optional[bool] = False
    """If true, treat pattern as literal. If false (default), treat as regex."""

    def to_polars(self) -> pl.Expr:
        """Converts the expression to a Polars str.replace or str.replace_all expression."""
        polars_value = self.value.to_polars()

        if isinstance(self.pattern, Expression):
            polars_pattern = self.pattern.to_polars()
        else:
            polars_pattern = pl.lit(self.pattern)

        if isinstance(self.replacement, Expression):
            polars_replacement = self.replacement.to_polars()
        else:
            polars_replacement = pl.lit(self.replacement)

        use_literal = self.literal or False

        if self.replace_all:
            return polars_value.str.replace_all(
                pattern=polars_pattern,
                value=polars_replacement,
                literal=use_literal
            )
        else:
            # Polars' replace takes 'n' for number of replacements. n=1 for first match.
            return polars_value.str.replace(
                pattern=polars_pattern,
                value=polars_replacement,
                literal=use_literal,
                n=1
            )
