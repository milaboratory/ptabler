from cmath import log
import typing
import operator
import polars as pl

from .base import Expression


# Comparison Expressions
ComparisonOperator = typing.Literal['gt', 'ge', 'eq', 'lt', 'le', 'neq']

_COMPARISON_OPERATORS_MAP: typing.Mapping[ComparisonOperator, typing.Callable[[pl.Expr, pl.Expr], pl.Expr]] = {
    "gt": operator.gt,
    "ge": operator.ge,
    "eq": operator.eq,
    "lt": operator.lt,
    "le": operator.le,
    "neq": operator.ne,
}

class GtExpression(Expression, tag='gt', tag_field="type", rename="camel"):
    lhs: Expression
    rhs: Expression

    def to_polars(self) -> pl.Expr:
        op = _COMPARISON_OPERATORS_MAP[self.type]
        return op(self.lhs.to_polars(), self.rhs.to_polars())

class GeExpression(GtExpression, tag='ge'): pass
class EqExpression(GtExpression, tag='eq'): pass
class LtExpression(GtExpression, tag='lt'): pass
class LeExpression(GtExpression, tag='le'): pass
class NeqExpression(GtExpression, tag='neq'): pass


# Binary Arithmetic Expressions
BinaryArithmeticOperator = typing.Literal['plus', 'minus', 'multiply', 'truediv', 'floordiv']

_BINARY_ARITHMETIC_OPERATORS_MAP: typing.Mapping[BinaryArithmeticOperator, typing.Callable[[pl.Expr, pl.Expr], pl.Expr]] = {
    "plus": operator.add,
    "minus": operator.sub,
    "multiply": operator.mul,
    "truediv": operator.truediv,
    "floordiv": operator.floordiv,
}

class PlusExpression(Expression, tag='plus', tag_field="type", rename="camel"):
    lhs: Expression
    rhs: Expression

    def to_polars(self) -> pl.Expr:
        op = _BINARY_ARITHMETIC_OPERATORS_MAP[self.type]
        return op(self.lhs.to_polars(), self.rhs.to_polars())

class MinusExpression(PlusExpression, tag='minus'): pass
class MultiplyExpression(PlusExpression, tag='multiply'): pass
class TrueDivExpression(PlusExpression, tag='truediv'): pass
class FloorDivExpression(PlusExpression, tag='floordiv'): pass


# Unary Arithmetic Expressions
UnaryArithmeticOperator = typing.Literal['log10', 'log', 'log2', 'abs', 'sqrt', 'minus']

class UnaryArithmeticBaseExpression(Expression, tag_field="type", rename="camel"):
    value: Expression

class Log10Expression(UnaryArithmeticBaseExpression, tag='log10'):
    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().log10()

class LogExpression(UnaryArithmeticBaseExpression, tag='log'):
    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().log()

class Log2Expression(UnaryArithmeticBaseExpression, tag='log2'):
    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().log() / pl.lit(log(2))

class AbsExpression(UnaryArithmeticBaseExpression, tag='abs'):
    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().abs()

class SqrtExpression(UnaryArithmeticBaseExpression, tag='sqrt'):
    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().sqrt()

class UnaryMinusExpression(UnaryArithmeticBaseExpression, tag='minus'):
    def to_polars(self) -> pl.Expr:
        return -self.value.to_polars() # Unary minus operator


# Boolean Logic Expressions

class AndExpression(Expression, tag='and', rename="camel"):
    operands: list[Expression]

    def to_polars(self) -> pl.Expr:
        polars_operands = [op.to_polars() for op in self.operands]
        if not polars_operands:
             # Define behavior for empty operands: 'and' -> True
             return pl.lit(True)
        return pl.all_horizontal(polars_operands)

class OrExpression(Expression, tag='or', rename="camel"):
    operands: list[Expression]

    def to_polars(self) -> pl.Expr:
        polars_operands = [op.to_polars() for op in self.operands]
        if not polars_operands:
            # Define behavior for empty operands: 'or' -> False
            return pl.lit(False)
        return pl.any_horizontal(polars_operands)


# Not Expression
class NotExpression(Expression, tag='not', rename="camel"):
    value: Expression

    def to_polars(self) -> pl.Expr:
        # Use bitwise NOT operator (~) which acts as logical NOT for boolean expressions in Polars
        return ~self.value.to_polars()


# Null Check Expressions

class IsNaExpression(Expression, tag='is_na', rename="camel"):
    value: Expression

    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().is_null()

class IsNotNaExpression(Expression, tag='is_not_na', rename="camel"):
    value: Expression

    def to_polars(self) -> pl.Expr:
        return self.value.to_polars().is_not_null()


# Column Reference Expression
class ColumnReferenceExpression(Expression, tag='col', rename="camel"):
    name: str

    def to_polars(self) -> pl.Expr:
        return pl.col(self.name)


# Constant Value Expression
class ConstantValueExpression(Expression, tag='const', rename="camel"):
    value: typing.Union[str, int, float, bool, None]

    def to_polars(self) -> pl.Expr:
        return pl.lit(self.value)


# Min/Max Expressions

class MinExpression(Expression, tag='min', rename="camel"):
    operands: list[Expression]

    def to_polars(self) -> pl.Expr:
        polars_operands = [op.to_polars() for op in self.operands]
        if not polars_operands:
            return pl.lit(None)
        return pl.min_horizontal(polars_operands)

class MaxExpression(Expression, tag='max', rename="camel"):
    operands: list[Expression]

    def to_polars(self) -> pl.Expr:
        polars_operands = [op.to_polars() for op in self.operands]
        if not polars_operands:
            return pl.lit(None)
        return pl.max_horizontal(polars_operands)
