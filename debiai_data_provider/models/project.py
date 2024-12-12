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

    def get_structure(self) -> dict:
        raise NotImplementedError

    def get_data(self) -> pd.DataFrame:
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
        try:
            nbSamples = self.project.get_data().shape[0]
        except NotImplementedError:
            nbSamples = 0

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
        try:
            structure = self.project.get_structure()
        except NotImplementedError:
            structure = None

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
            nbSamples=None,
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

        # Display the project data shape
        data = self.get_data()
        data_columns_text = "\n".join(data.columns)
        table.add_row("Data:", "")
        table.add_row("Shape:", str(data.shape))
        table.add_row("Columns:", data_columns_text)
        table.add_row("", "")

        return table
