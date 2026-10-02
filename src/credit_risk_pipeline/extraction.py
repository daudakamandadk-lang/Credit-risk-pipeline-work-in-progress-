"""Prototype extraction boundary for the governed credit-risk pipeline."""

from dataclasses import dataclass,field
from enum import Enum
from pathlib import Path
from typing import Any
import pandas as pd

class SourceType(str,Enum):
    CSV="csv"
    JSON="json"
    EXCEL="excel"
    PARQUET="parquet"

class ExtractionStatus(str,Enum):
    SUCCESS="SUCCESS"
    FAILED="FAILED"

@dataclass
class SourceConfig:
    source_type:SourceType
    path:str
    options:dict[str,Any]=field(default_factory=dict)

@dataclass
class ExtractionMetadata:
    source_name:str
    row_count:int
    column_count:int
    columns:list[str]

@dataclass
class ExtractionResult:
    status:ExtractionStatus
    data:pd.DataFrame|None
    metadata:ExtractionMetadata|None
    errors:list[str]=field(default_factory=list)

class ExtractionEngine:
    """Read a configured file source and return data plus extraction metadata."""

    def __init__(self):
        self.readers={
            SourceType.CSV:pd.read_csv,
            SourceType.JSON:pd.read_json,
            SourceType.EXCEL:pd.read_excel,
            SourceType.PARQUET:pd.read_parquet
        }

    def validate_source(self,config):
        path=Path(config.path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return path

    def build_metadata(self,path,data):
        return ExtractionMetadata(
            source_name=path.name,
            row_count=len(data),
            column_count=len(data.columns),
            columns=data.columns.tolist()
        )

    def extract(self,config):
        try:
            path=self.validate_source(config)
            reader=self.readers[config.source_type]
            data=reader(path,**config.options)
            metadata=self.build_metadata(path,data)
            return ExtractionResult(
                status=ExtractionStatus.SUCCESS,
                data=data,
                metadata=metadata
            )
        except Exception as error:
            return ExtractionResult(
                status=ExtractionStatus.FAILED,
                data=None,
                metadata=None,
                errors=[str(error)]
            )
