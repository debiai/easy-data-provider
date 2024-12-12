from fastapi import APIRouter, Depends, Request
from typing import List, Dict, Optional, Union
from fastapi import Path, Query, Body
from debiai_data_provider.models.debiai import (
    InfoResponse,
    CanDelete,
    ProjectOverview,
    ProjectDetail,
    ModelDetail,
    SelectionRequest,
)
from debiai_data_provider.app import APP_VERSION
from debiai_data_provider.data_provider import DataProvider

router = APIRouter()


def get_data_provider(request: Request):
    return request.app.state.data_provider


# Info routes
@router.get("/info", response_model=InfoResponse, tags=["Info"])
def get_info():
    return InfoResponse(
        version=APP_VERSION,
        maxSampleIdByRequest=10000,
        maxSampleDataByRequest=2000,
        maxResultByRequest=5000,
        canDelete=CanDelete(),
    )


# Project routes
@router.get("/projects", response_model=Dict[str, ProjectOverview], tags=["Projects"])
def get_projects(data_provider: DataProvider = Depends(get_data_provider)):
    debiai_projects = data_provider.projects
    return {
        project.project_name: project.project.get_overview()
        for project in debiai_projects
    }


@router.get("/projects/{projectId}", response_model=ProjectDetail, tags=["Projects"])
def get_project(projectId: str = Path(..., min_length=1, example="Project 1")):
    return {}


@router.delete("/projects/{projectId}", status_code=200, tags=["Projects"])
def delete_project(projectId: str = Path(..., min_length=1, example="Project 1")):
    return {"message": "Project deleted"}


# Data routes
@router.get(
    "/projects/{projectId}/data-id-list",
    response_model=List[Union[str, int]],
    tags=["Data"],
)
def get_data_id_list(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    from_: Optional[int] = Query(None),
    to: Optional[int] = Query(None),
    analysisId: Optional[str] = Query(None),
    analysisStart: Optional[bool] = Query(None),
    analysisEnd: Optional[bool] = Query(None),
):
    return []


@router.post(
    "/projects/{projectId}/data",
    response_model=Dict[str, List[Union[str, int, float]]],
    tags=["Data"],
)
def post_data(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    body: List[Union[str, int, float]] = Body(...),
):
    return {}


# Model routes
@router.get(
    "/projects/{projectId}/models",
    response_model=List[ModelDetail],
    tags=["Models"],
)
def get_models(projectId: str = Path(..., min_length=1, example="Project 1")):
    return []


@router.post(
    "/projects/{projectId}/models/{modelId}/results",
    response_model=Dict[str, List[Union[str, int, float, bool]]],
    tags=["Models"],
)
def post_model_results(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    modelId: str = Path(..., min_length=1, example="Model 1"),
    body: List[Union[str, int, float]] = Body(...),
):
    return {}


@router.delete(
    "/projects/{projectId}/models/{modelId}", status_code=204, tags=["Models"]
)
def delete_model(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    modelId: str = Path(..., min_length=1, example="Model 1"),
):
    return {"message": "Model deleted"}


# Selection routes
@router.get(
    "/projects/{projectId}/selections",
    response_model=List[Dict[str, Union[str, int]]],
    tags=["Selections"],
)
def get_selections(projectId: str = Path(..., min_length=1, example="Project 1")):
    return []


@router.post("/projects/{projectId}/selections", status_code=204, tags=["Selections"])
def create_selection(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    body: SelectionRequest = Body(...),
):
    return {"message": "Selection created successfully"}


@router.delete(
    "/projects/{projectId}/selections/{selectionId}",
    status_code=204,
    tags=["Selections"],
)
def delete_selection(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    selectionId: str = Path(..., min_length=1, example="Selection 1"),
):
    return {"message": "Selection deleted"}