from .base import PStep, GlobalSettings, TableSpace
from .io import ReadCsv, WriteCsv, WriteJson
from .basics import AddColumns, Select, WithColumns, WithoutColumns
from .filter import Filter
from .join import Join
from .aggregate import Aggregate
from .concatenate import Concatenate
from .sort import Sort

from typing import Union

type AnyPStep = Union[ReadCsv, WriteCsv,
                      WriteJson, AddColumns, Select, WithColumns, Filter, Join, Aggregate, Concatenate, Sort, WithoutColumns]

__all__ = ["PStep", "ReadCsv", "WriteCsv", "WriteJson", "AddColumns", "Select", "WithColumns", "WithoutColumns",
           "Filter", "Join", "Aggregate", "Concatenate", "Sort", "GlobalSettings", "TableSpace", "AnyPStep"]
