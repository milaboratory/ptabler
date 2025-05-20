from .base import PStep, GlobalSettings, TableSpace
from .io import ReadCsv, WriteCsv, WriteJson
from .add_columns import AddColumns
from .filter import Filter
from .join import Join
from .aggregate import Aggregate
from .concatenate import Concatenate

from typing import Union

type AnyPStep = Union[ReadCsv, WriteCsv,
                      WriteJson, AddColumns, Filter, Join, Aggregate, Concatenate]

__all__ = ["PStep", "ReadCsv", "WriteCsv", "WriteJson", "AddColumns",
           "Filter", "Join", "Aggregate", "Concatenate", "GlobalSettings", "TableSpace", "AnyPStep"]
