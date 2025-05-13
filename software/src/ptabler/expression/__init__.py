from .base import Expression

from .basics import (
    GtExpression,
    GeExpression,
    EqExpression,
    LtExpression,
    LeExpression,
    NeqExpression,
    PlusExpression,
    MinusExpression,
    MultiplyExpression,
    TrueDivExpression,
    FloorDivExpression,
    Log10Expression,
    LogExpression,
    Log2Expression,
    AbsExpression,
    SqrtExpression,
    UnaryMinusExpression,
    AndExpression,
    OrExpression,
    NotExpression,
    IsNaExpression,
    IsNotNaExpression,
    ColumnReferenceExpression,
    ConstantValueExpression,
    MinExpression,
    MaxExpression,
)
from .string import (
    StringJoinExpression,
    ToUpperExpression,
    ToLowerExpression,
    StrLenExpression,
    SubstringExpression,
)
from .fuzzy import (
    StringDistanceExpression,
    FuzzyStringFilterExpression,
)
from .conditional import WhenThenOtherwiseExpression
from .window import RankExpression, CumsumExpression
from .hash import HashExpression

import typing

# Define a Union type that includes all concrete expression types
AnyExpression = typing.Union[
    # Basic Comparisons
    GtExpression,
    GeExpression,
    EqExpression,
    LtExpression,
    LeExpression,
    NeqExpression,
    # Basic Binary Arithmetic
    PlusExpression,
    MinusExpression,
    MultiplyExpression,
    TrueDivExpression,
    FloorDivExpression,
    # Basic Unary Arithmetic
    Log10Expression,
    LogExpression,
    Log2Expression,
    AbsExpression,
    SqrtExpression,
    UnaryMinusExpression,
    # Boolean Logic
    AndExpression,
    OrExpression,
    NotExpression,
    # Null Checks
    IsNaExpression,
    IsNotNaExpression,
    # Core Types
    ColumnReferenceExpression,
    ConstantValueExpression,
    # Min/Max
    MinExpression,
    MaxExpression,
    # String Operations
    StringJoinExpression,
    ToUpperExpression,
    ToLowerExpression,
    StrLenExpression,
    SubstringExpression,
    # Fuzzy String Operations
    StringDistanceExpression,
    FuzzyStringFilterExpression,
    # Conditional Logic
    WhenThenOtherwiseExpression,
    # Window Functions
    RankExpression,
    CumsumExpression,
    # Hash Functions
    HashExpression,
    # String Distance Functions
    StringDistanceExpression,
    FuzzyStringFilterExpression,
]

__all__ = [
    "Expression",
    "AnyExpression"
    "GtExpression",
    "GeExpression",
    "EqExpression",
    "LtExpression",
    "LeExpression",
    "NeqExpression",
    "PlusExpression",
    "MinusExpression",
    "MultiplyExpression",
    "TrueDivExpression",
    "FloorDivExpression",
    "Log10Expression",
    "LogExpression",
    "Log2Expression",
    "AbsExpression",
    "SqrtExpression",
    "UnaryMinusExpression",
    "AndExpression",
    "OrExpression",
    "NotExpression",
    "IsNaExpression",
    "IsNotNaExpression",
    "ColumnReferenceExpression",
    "ConstantValueExpression",
    "MinExpression",
    "MaxExpression",
    "StringJoinExpression",
    "ToUpperExpression",
    "ToLowerExpression",
    "StrLenExpression",
    "SubstringExpression",
    "StringDistanceExpression",
    "FuzzyStringFilterExpression",
    "WhenThenOtherwiseExpression",
    "RankExpression",
    "CumsumExpression",
    "HashExpression",
    "StringDistanceExpression",
    "FuzzyStringFilterExpression"
]
