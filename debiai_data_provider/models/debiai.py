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
    metadata: Optional[dict] = {}
    metrics: Optional[dict] = {}
    tags: Optional[list] = []
    type: Optional[str] = "auto"


class ExpectedResult(BaseModel):
    name: str
    type: str = "auto"
    group: Optional[str] = ""


class ProjectDetails(BaseModel):
    id: Optional[str]
    dataProviderId: Optional[str]
    name: Optional[str]
    columns: List[Column]
    expectedResults: List[ExpectedResult]
    nbSamples: Optional[int] = None
    creationDate: Optional[int] = None
    updateDate: Optional[int] = None
    models: Optional[list] = []
    selections: Optional[list] = []
    metrics: Optional[dict] = {}
    tags: Optional[list] = []
    metadata: Optional[dict] = {}


class ModelDetail(BaseModel):
    id: str
    name: Optional[str]
    nbResults: Optional[int] = None
    creationDate: Optional[int] = None


class SelectionRequest(BaseModel):
    name: str
    idList: List[str]
