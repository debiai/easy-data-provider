from pydantic import BaseModel
from typing import List, Optional


class CanDelete(BaseModel):
    projects: bool = True
    selections: bool = True
    models: bool = True


class InfoResponse(BaseModel):
    version: str
    maxSampleIdByRequest: int = 10000
    maxSampleDataByRequest: int = 2000
    maxResultByRequest: int = 5000
    canDelete: CanDelete


class ProjectOverview(BaseModel):
    name: Optional[str]
    nbSamples: Optional[int] = None
    nbModels: Optional[int] = None
    nbSelections: Optional[int] = None
    creationDate: Optional[int] = None
    updateDate: Optional[int] = None


class Column(BaseModel):
    name: str
    category: str = "other"
    type: Optional[str] = "auto"
    group: Optional[str] = None


class ExpectedResult(BaseModel):
    name: str
    type: str = "auto"
    group: Optional[str] = ""


class ProjectDetails(BaseModel):
    name: Optional[str]
    columns: List[Column]
    expectedResults: List[ExpectedResult]
    nbSamples: Optional[int] = None
    creationDate: Optional[int] = None
    updateDate: Optional[int] = None


class ModelDetail(BaseModel):
    id: str
    name: Optional[str]
    nbResults: Optional[int] = None
    creationDate: Optional[int] = None


class SelectionRequest(BaseModel):
    name: str
    idList: List[str]
