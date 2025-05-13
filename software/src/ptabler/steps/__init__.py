from .base import PStep, GlobalSettings, TableSpace
from .io import ReadCsv, WriteCsv

from typing import Union

type AnyPStep = Union[ReadCsv, WriteCsv]

__all__ = ["PStep", "ReadCsv", "WriteCsv", "GlobalSettings", "TableSpace", "AnyPStep"]
