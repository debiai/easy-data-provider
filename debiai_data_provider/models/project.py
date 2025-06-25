import pandas as pd
from rich.table import Table
from debiai_data_provider.models.debiai import (
    ProjectOverview,
    ProjectDetails,
    ModelDetail,
    Column,
    ExpectedResult,
)
from typing import Optional, Union, List, Tuple, Dict


class DebiAIProject:
    creation_date: Optional[Union[None, str]] = None
    update_date: Optional[Union[None, str]] = None
    name: Optional[str] = None

    # Project information
    def get_structure(self) -> dict:
        raise NotImplementedError

    def get_results_structure(self) -> dict:
        return {}

    # Project actions
    def delete_project(self):
        raise NotImplementedError

    # Project Samples
    def get_nb_samples(self) -> Union[int, None]:
        return None

    def get_samples_ids(self) -> List[str]:
        raise NotImplementedError

    def get_data(self, samples_ids: List[str]) -> pd.DataFrame:
        raise NotImplementedError

    # Project models
    def get_models(self) -> List[ModelDetail]:
        return []

    def get_model_evaluated_data_id_list(self, model_id: str) -> List[str]:
        raise NotImplementedError

    def get_model_results(self, model_id: str, sample_ids: List[str]) -> pd.DataFrame:
        raise NotImplementedError


class ProjectToExpose:
    def __init__(self, project: DebiAIProject, project_name: str):
        self.project = project
        self.project_name = project_name

    # Getters
    def get_columns(self) -> Union[List[Column], None]:
        try:
            structure = self.project.get_structure()
        except NotImplementedError:
            return None

        if not isinstance(structure, dict):
            raise ValueError("The 'get_structure' method must return a dictionary.")

        structure = structure.copy()

        for key, value in structure.items():
            if not isinstance(value, dict):
                raise ValueError(
                    f"Error in the structure of the column '{key}', it must be a dictionary."
                )

            if "category" not in value:
                # Set the default category to "other"
                value["category"] = "other"
            else:
                if not isinstance(value["category"], str):
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'category' must be a string."
                    )

                if value["category"] not in [
                    "context",
                    "input",
                    "groundtruth",
                    "other",
                ]:
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'category' must be 'context', 'input', 'groundtruth' or 'other'."  # noqa
                    )

            if "type" in value:
                if not isinstance(value["type"], str):
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'type' must be a string."
                    )

                VALID_TYPES = ["text", "number", "bool", "dict", "list", "auto"]
                if value["type"] not in VALID_TYPES:
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'type' must be "
                        + ", ".join(VALID_TYPES)
                        + "."
                    )

            if "group" in value:
                if not isinstance(value["group"], str):
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'group' must be a string."
                    )

        # Convert:
        # {
        #     "col_name": {
        #         "type": "text",
        #         "category": "context",
        #         "group": "context",
        #     },
        #     ...
        # }
        # to:
        # [
        #     Column(name="col_name", type="text", category="context", group="context"),
        # ]

        columns = []
        for key, value in structure.items():
            columns.append(
                Column(
                    name=key,
                    category=value["category"],
                    type=value["type"],
                    group=value.get("group", ""),
                )
            )

        return columns

    def get_results_columns(self) -> Union[List[ExpectedResult], None]:
        try:
            structure = self.project.get_results_structure()
        except NotImplementedError:
            return None

        if not isinstance(structure, dict):
            raise ValueError(
                f'The "get_results_structure" method must return a dictionary, got {type(structure)}.\n\
Expected dictionary format: {{"col_name": {{"type": text, "group": text}}}}.'
            )

        structure = structure.copy()

        for key, value in structure.items():
            if not isinstance(value, dict):
                raise ValueError(
                    f"Error in the structure of the column '{key}', it must be a dictionary."
                )

            if "type" in value:
                if not isinstance(value["type"], str):
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'type' must be a string."
                    )

                VALID_TYPES = ["text", "number", "bool", "dict", "list", "auto"]
                if value["type"] not in VALID_TYPES:
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'type' must be "
                        + ", ".join(VALID_TYPES)
                        + "."
                    )

            if "group" in value:
                if not isinstance(value["group"], str):
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'group' must be a string."
                    )
        # Convert:
        # {
        #     "col_name": {
        #         "type": "text",
        #         "group": "context",
        #     },
        #     ...
        # }
        # to:
        # [
        #     ExpectedResult(name="col_name", type="text", group="context"),
        # ]

        columns = []
        for key, value in structure.items():
            columns.append(
                ExpectedResult(
                    name=key,
                    type=value["type"],
                    group=value.get("group", ""),
                )
            )

        return columns

    def get_nb_samples(self) -> Union[int, None]:
        nb_samples = self.project.get_nb_samples()

        if nb_samples is None or not isinstance(nb_samples, int):
            return None

        return nb_samples

    def get_samples_ids(self) -> List[str]:
        try:
            samples_id = self.project.get_samples_ids()
        except NotImplementedError:
            return []

        if not isinstance(samples_id, list):
            raise ValueError("The 'get_samples_ids' method must return a list.")

        # Ids must be strings or integers
        if not all(isinstance(x, (str, int)) for x in samples_id):
            raise ValueError(
                "The 'get_samples_ids' method must return a list of strings."
            )

        return samples_id

    # Project information
    def get_dates(self) -> Tuple[Optional[int], Optional[int]]:
        # Get the creation date
        creationDate = None
        if self.project.creation_date is not None and isinstance(
            self.project.creation_date, str
        ):
            # Convert the creation date to a timestamp
            creationDate = pd.Timestamp(self.project.creation_date).timestamp() * 1000

        # Get update date
        updateDate = None
        if self.project.update_date is not None and isinstance(
            self.project.update_date, str
        ):
            # Convert the update date to a timestamp
            updateDate = pd.Timestamp(self.project.update_date).timestamp() * 1000

        return creationDate, updateDate

    def get_overview(self) -> ProjectOverview:
        # Get project details
        creationDate, updateDate = self.get_dates()

        # Get the number of samples
        nbSamples = self.get_nb_samples()

        # Get models details
        models = self.get_models()

        return ProjectOverview(
            name=self.project_name,
            nbSamples=nbSamples,
            nbModels=len(models),
            nbSelections=None,
            creationDate=creationDate,
            updateDate=updateDate,
        )

    def get_details(self) -> ProjectDetails:
        # Get project details
        creationDate, updateDate = self.get_dates()

        # Get the number of samples
        nbSamples = self.get_nb_samples()

        # Construct the project columns
        columns = self.get_columns()
        results_columns = self.get_results_columns()

        return ProjectDetails(
            name=self.project_name,
            columns=columns,
            expectedResults=results_columns,
            nbSamples=nbSamples,
            creationDate=creationDate,
            updateDate=updateDate,
        )

    # Samples
    def get_data_id_list(
        self,
        from_: Optional[int] = None,
        to: Optional[int] = None,
        analysisId: Optional[str] = None,
        analysisStart: Optional[bool] = None,
        analysisEnd: Optional[bool] = None,
    ) -> List[str]:
        samples_ids = self.get_samples_ids()

        if from_ is not None and to is not None:
            samples_ids = samples_ids[from_ : to + 1]  # noqa

        elif from_ is not None:
            samples_ids = samples_ids[from_:]

        elif to is not None:
            samples_ids = samples_ids[: to + 1]

        return samples_ids

    def get_data_from_ids(self, samples_ids: List[str]) -> dict:
        from debiai_data_provider.utils.parser import dataframe_to_debiai_data

        # Get the data from the project
        df_data = self.project.get_data(samples_ids)

        # Create a copy of the dataframe
        df_data = df_data.copy()

        # Verify that all the columns are in the dataframe
        columns = self.get_columns()
        if not columns:
            raise ValueError("The project has no columns defined.")

        for column in columns:
            if column.name not in df_data.columns:
                # Add the column to the dataframe
                df_data[column.name] = None

        return dataframe_to_debiai_data(
            columns=columns, samples_id=samples_ids, data=df_data
        )

    # Models
    def get_models(self) -> List[ModelDetail]:
        models = self.project.get_models()

        # Convert the models to ModelDetail
        model_details = []
        for model in models:
            if isinstance(model, ModelDetail):
                model_details.append(model)
            elif isinstance(model, dict):
                if "id" not in model:
                    raise ValueError("The model must have an 'id' key.")

                model_details.append(
                    ModelDetail(
                        id=model["id"],
                        name=model.get("name", None),
                        nbResults=model.get("nb_results", None),
                        creationDate=model.get("creation_date", None),
                    )
                )
            else:
                raise ValueError("The model must be a ModelDetail or a dictionary.")

        return model_details

    def get_model_evaluated_data_id_list(self, model_id: str) -> List[str]:
        return self.project.get_model_evaluated_data_id_list(model_id)

    def get_model_results(
        self, model_id: str, sample_ids: List[str]
    ) -> Dict[str, list]:
        df_results = self.project.get_model_results(model_id, sample_ids)

        # Convert the dataframe to a list of dictionaries
        results = df_results.to_dict(orient="records")
        # Results:
        # {
        #     s_id: {
        #         "res_col_1": "OK",
        #         "res_col_2": 0.05,
        #         "res_col_3": 0.94,
        #         ...
        #     },
        #     "..."
        # }

        # Convert to list with same order as results columns:
        # {
        #     s_id: ["OK", 0.05, 0.94, ...],
        #     "..."
        # }
        results_dict = {}
        results_columns = self.get_results_columns()

        for sample_id, result in zip(sample_ids, results):
            results_list = []

            for column in results_columns:
                if column.name in result:
                    results_list.append(result[column.name])
                else:
                    results_list.append(None)

            results_dict[sample_id] = results_list

        return results_dict

    # Other
    def get_rich_table(self):
        # Display the Project details
        table = Table(width=80)
        table.add_column(
            self.project_name, style="cyan", no_wrap=True, justify="right", width=20
        )

        # Get updated and creation date
        creation_update_text = ""
        if self.project.creation_date:
            creation_update_text += (
                f"Created: {pd.Timestamp(self.project.creation_date).date()} "
            )
        if self.project.update_date:
            creation_update_text += (
                f"Updated: {pd.Timestamp(self.project.update_date).date()}"
            )
        table.add_column(creation_update_text, width=60)

        # Display the project column structure
        columns = self.get_columns()
        if columns:
            table.add_row("Structure:", "")
            for column in columns:
                column_value = (
                    f"[bold blue]{column.type}[/bold blue] "
                    + f"[italic]{column.category}[/italic]"
                )
                if column.group:
                    column_value += f" [blue]<{column.group}>[/blue]"

                table.add_row(
                    f"[bold green]{column.name}[/bold green]",
                    column_value,
                )
            table.add_row("", "")

        # Display the project data number of samples
        nb_samples = self.get_nb_samples()
        if nb_samples is not None:
            table.add_row("NB samples:", f"{nb_samples}")
            table.add_row("", "")

        # Display the project results structure
        results_columns = self.get_results_columns()
        if results_columns:
            table.add_row("Results:", "")
            for column in results_columns:
                column_value = f"[bold blue]{column.type}[/bold blue] "
                if column.group:
                    column_value += f" [blue]<{column.group}>[/blue]"

                table.add_row(
                    f"[bold green]{column.name}[/bold green]",
                    column_value,
                )
            table.add_row("", "")

        # Display the project models
        models = self.get_models()
        if models:
            table.add_row("Models:", "")
            for model in models:
                model_value = f"[bold blue]{model.id}[/bold blue]"
                if model.name:
                    model_value += f" [italic]{model.name}[/italic]"
                if model.creationDate:
                    model_value += f" ({pd.Timestamp(model.creationDate).date()})"
                if model.nbResults:
                    model_value += f" ({model.nbResults} results)"

                table.add_row(
                    f"[bold green]{model.id}[/bold green]",
                    model_value,
                )
            table.add_row("", "")

        return table
