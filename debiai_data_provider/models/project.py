import pandas as pd
from rich.table import Table
from debiai_data_provider.models.debiai import (
    ProjectOverview,
    ProjectDetails,
    Column,
)
from typing import Optional, Union


class DebiAIProject:
    creation_date: Optional[Union[None, str]] = None

    # Project information
    def get_structure(self) -> dict:
        raise NotImplementedError

    # Project actions
    def delete_project(self):
        raise NotImplementedError

    # Project Samples
    def get_nb_samples(self) -> Union[int, None]:
        return None

    def get_samples_ids(self) -> list[str]:
        raise NotImplementedError

    def get_data(self, samples_ids: list[str]) -> pd.DataFrame:
        raise NotImplementedError


class ProjectToExpose:
    def __init__(self, project: DebiAIProject, project_name: str):
        self.project = project
        self.project_name = project_name

    # Getters
    def get_columns(self) -> Union[list[Column], None]:
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
                        f"Error in the structure of the column '{key}', the 'category' must be 'context', 'input', 'groundtruth' or 'other'."
                    )

            if "type" in value:
                if not isinstance(value["type"], str):
                    raise ValueError(
                        f"Error in the structure of the column '{key}', the 'type' must be a string."
                    )

                VALID_TYPES = ["text", "number", "bool", "dict", "list"]
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

    def get_nb_samples(self) -> Union[int, None]:
        nb_samples = self.project.get_nb_samples()

        if nb_samples is None or not isinstance(nb_samples, int):
            return None

        return nb_samples

    def get_samples_ids(self) -> list[str]:
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
    def get_overview(self) -> ProjectOverview:
        # Get the number of samples
        nbSamples = self.get_nb_samples()

        # Get the creation date
        creationDate = None
        if self.project.creation_date is not None and isinstance(
            self.project.creation_date, str
        ):
            # Convert the creation date to a timestamp
            creationDate = pd.Timestamp(self.project.creation_date).timestamp() * 1000

        return ProjectOverview(
            name=self.project_name,
            nbSamples=nbSamples,
            nbModels=None,
            nbSelections=None,
            creationDate=creationDate,
            updateDate=None,
        )

    def get_details(self) -> ProjectDetails:
        # Get the number of samples
        nbSamples = self.get_nb_samples()

        # Construct the project columns
        columns = self.get_columns()

        return ProjectDetails(
            name=self.project_name,
            columns=columns,
            expectedResults=[],
            nbSamples=nbSamples,
            creationDate=None,
            updateDate=None,
        )

    # Project samples
    def get_data_id_list(
        self,
        from_: Optional[int] = None,
        to: Optional[int] = None,
        analysisId: Optional[str] = None,
        analysisStart: Optional[bool] = None,
        analysisEnd: Optional[bool] = None,
    ) -> list[str]:
        samples_ids = self.get_samples_ids()

        if from_ is not None and to is not None:
            samples_ids = samples_ids[from_ : to + 1]  # noqa

        elif from_ is not None:
            samples_ids = samples_ids[from_:]

        elif to is not None:
            samples_ids = samples_ids[: to + 1]

        return samples_ids

    def get_data_from_ids(self, samples_ids: list[str]) -> dict:
        from debiai_data_provider.utils.parser import dataframe_to_debiai_data_array

        # Get the data from the project
        df_data = self.project.get_data(samples_ids)

        # Create a copy of the dataframe
        df_data = df_data.copy()

        # Verify that all the columns are in the dataframe
        columns = self.get_columns()
        for column in columns:
            if column.name not in df_data.columns:
                # Add the column to the dataframe
                df_data[column.name] = None

        return dataframe_to_debiai_data_array(
            columns=self.get_columns(), samples_id=samples_ids, data=df_data
        )

    # Other
    def get_rich_table(self):
        # Display the Project details
        table = Table(width=80)
        table.add_column(
            self.project_name, style="cyan", no_wrap=True, justify="right", width=20
        )
        table.add_column("", width=60)

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
                    column_value += f" [blue]\[{column.group}][/blue]"

                table.add_row(
                    f"[bold green]{column.name}[/bold green]",
                    column_value,
                )
            table.add_row("", "")

        # Display the project data number of samples
        nb_samples = self.get_nb_samples()
        if nb_samples is not None:
            table.add_row("NB samples:", f"{nb_samples}")

        return table
