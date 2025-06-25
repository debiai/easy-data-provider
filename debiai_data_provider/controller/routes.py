from fastapi import APIRouter, Depends, Request
from typing import List, Dict, Optional, Union
from fastapi import Path, Query, Body
from debiai_data_provider.models.debiai import (
    InfoResponse,
    CanDelete,
    ProjectOverview,
    ProjectDetails,
    ModelDetail,
    SelectionRequest,
)
from debiai_data_provider.version import VERSION
from debiai_data_provider.data_provider import DataProvider

router = APIRouter()


def get_data_provider(request: Request):
    return request.app.state.data_provider


# Info routes
@router.get("/info", response_model=InfoResponse, tags=["Info"])
def get_info(data_provider: DataProvider = Depends(get_data_provider)):
    return InfoResponse(
        version=VERSION,
        maxSampleIdByRequest=data_provider.max_sample_id_by_request or 10000,
        maxSampleDataByRequest=data_provider.max_sample_data_by_request or 2000,
        maxResultByRequest=data_provider.max_result_by_request or 5000,
        canDelete=CanDelete(),
    )


# Project routes
@router.get("/projects", response_model=Dict[str, ProjectOverview], tags=["Projects"])
def get_projects(data_provider: DataProvider = Depends(get_data_provider)):
    debiai_projects = data_provider.projects
    return {project.project_name: project.get_overview() for project in debiai_projects}


@router.get("/projects/{projectId}", response_model=ProjectDetails, tags=["Projects"])
def get_project(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    data_provider: DataProvider = Depends(get_data_provider),
):
    return data_provider._get_project_to_expose(projectId).get_details()


@router.delete("/projects/{projectId}", status_code=200, tags=["Projects"])
def delete_project(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    data_provider: DataProvider = Depends(get_data_provider),
):
    data_provider.delete_project(projectId)
    return {"message": "Project deleted"}


# Data routes
@router.get(
    "/projects/{projectId}/data-id-list",
    response_model=List[Union[str, int]],
    tags=["Data"],
)
def get_data_id_list(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    from_: Optional[int] = Query(None, alias="from"),
    to: Optional[int] = Query(None),
    analysisId: Optional[str] = Query(None),
    analysisStart: Optional[bool] = Query(None),
    analysisEnd: Optional[bool] = Query(None),
    data_provider: DataProvider = Depends(get_data_provider),
):
    project = data_provider._get_project_to_expose(projectId)
    return project.get_data_id_list(from_, to, analysisId, analysisStart, analysisEnd)


@router.post(
    "/projects/{projectId}/data",
    response_model=Dict[
        Union[str, int], List[Union[str, int, float, bool, None, list, dict]]
    ],
    tags=["Data"],
)
def get_data(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    samples_ids: List[Union[str, int, float]] = Body(...),
    data_provider: DataProvider = Depends(get_data_provider),
):
    project = data_provider._get_project_to_expose(projectId)
    return project.get_data_from_ids(samples_ids)


# Model routes
@router.get(
    "/projects/{projectId}/models",
    response_model=List[ModelDetail],
    tags=["Models"],
)
def get_models(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    data_provider: DataProvider = Depends(get_data_provider),
):
    project = data_provider._get_project_to_expose(projectId)
    return project.get_models()


@router.get(
    "/projects/{projectId}/models/{modelId}/evaluated-data-id-list",
    response_model=List[Union[str, int]],
    tags=["Models"],
)
def get_models_evaluated_data_id_list(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    modelId: str = Path(..., min_length=1, example="Model 1"),
    data_provider: DataProvider = Depends(get_data_provider),
):
    project = data_provider._get_project_to_expose(projectId)
    return project.get_model_evaluated_data_id_list(modelId)


@router.post(
    "/projects/{projectId}/models/{modelId}/results",
    response_model=Dict[Union[str, int], List[Union[str, int, float, bool]]],
    tags=["Models"],
)
def get_model_results(
    projectId: str = Path(..., min_length=1, example="Project 1"),
    modelId: str = Path(..., min_length=1, example="Model 1"),
    body: List[Union[str, int, float]] = Body(...),
    data_provider: DataProvider = Depends(get_data_provider),
):
    project = data_provider._get_project_to_expose(projectId)
    return project.get_model_results(modelId, body)


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
