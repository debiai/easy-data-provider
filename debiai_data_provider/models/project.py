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
    def get_structure(self) -> Union[dict, None]:
        try:
            return self.project.get_structure()
        except NotImplementedError:
            return None

    def get_nb_samples(self) -> Union[int, None]:
        nb_samples = self.project.get_nb_samples()

        if nb_samples is None or not isinstance(nb_samples, int):
            return None

        return nb_samples

    def get_data(self) -> pd.DataFrame:
        try:
            df_data = self.project.get_data()
        except NotImplementedError:
            # Return empty DataFrame
            return pd.DataFrame()

        # Assert that the data are in the correct format
        if not isinstance(df_data, pd.DataFrame):
            raise ValueError("The 'get_data' method must return a pandas DataFrame.")

        if df_data is None:
            return pd.DataFrame()

        return df_data

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
        structure = self.get_structure()

        columns = []
        if structure:
            for key, value in structure.items():
                columns.append(
                    Column(
                        name=key,
                        category=value["category"],
                        type=value["type"],
                        group=value.get("group", ""),
                    )
                )

        return ProjectDetails(
            name=self.project_name,
            columns=columns,
            expectedResults=[],
            nbSamples=nbSamples,
            creationDate=None,
            updateDate=None,
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
        structure = self.get_structure()
        if structure:
            table.add_row("Structure:", "")
            for key, value in structure.items():
                table.add_row(
                    f"[bold green]{key}[/bold green]",
                    f"[bold blue]{value['type']}[/bold blue] "
                    + f"[italic]{value['category']}[/italic]",
                )
            table.add_row("", "")

        # Display the project data number of samples
        nb_samples = self.get_nb_samples()
        if nb_samples is not None:
            table.add_row("NB samples:", f"{nb_samples}")

        return table
