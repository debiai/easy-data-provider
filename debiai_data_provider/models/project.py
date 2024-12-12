import pandas as pd
from rich.table import Table
from debiai_data_provider.models.debiai import (
    ProjectOverview,
)
from typing import Optional, Union


class DebiAIProject:
    creation_date: Optional[Union[None, str]] = None

    def get_structure(self) -> dict:
        raise NotImplementedError

    def get_data(self) -> pd.DataFrame:
        raise NotImplementedError

    def get_details(self):
        # Get the class name
        name = self.__class__.__name__

        # Get the project structure
        try:
            structure = self.get_structure()
        except NotImplementedError:
            structure = None

        # Get the project data
        try:
            data = self.get_data()
        except NotImplementedError:
            data = None

        # Project details
        table = Table(width=80)
        table.add_column(name, style="cyan", no_wrap=True, justify="right", width=20)
        table.add_column("", width=60)

        if structure:
            table.add_row("Structure:", "")
            for key, value in structure.items():
                table.add_row(
                    f"[bold green]{key}[/bold green]",
                    f"[bold blue]{value['type']}[/bold blue] "
                    + f"[italic]{value['category']}[/italic]",
                )
            table.add_row("", "")

        if data is not None:
            table.add_row("Data:", "")
            table.add_row("Shape:", str(data.shape))
            table.add_row("Columns:", str(data.columns))
            table.add_row("", "")

        return table

    def get_overview(self) -> ProjectOverview:
        try:
            nbSamples = self.get_data().shape[0]
        except NotImplementedError:
            nbSamples = 0

        creationDate = None
        if self.creation_date is not None and isinstance(self.creation_date, str):
            # Convert the creation date to a timestamp
            creationDate = pd.Timestamp(self.creation_date).timestamp() * 1000

        return ProjectOverview(
            name=self.__class__.__name__,
            nbSamples=nbSamples,
            nbModels=None,
            nbSelections=None,
            creationDate=creationDate,
            updateDate=None,
        )


class ProjectToExpose:
    def __init__(self, project: DebiAIProject, project_name: str):
        self.project = project
        self.project_name = project_name
