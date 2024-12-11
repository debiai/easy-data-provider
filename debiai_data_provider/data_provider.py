from typing import List
from debiai_data_provider.utils.parser import extract_project_metadata
from debiai_data_provider.models.project import DebiAIProject, ProjectToExpose
from debiai_data_provider.app import start_api_server
from rich.console import Console
from rich.panel import Panel


class DataProvider:
    def __init__(self):
        self.projects: List[ProjectToExpose] = []

    def add_project(
        self,
        project: DebiAIProject,
    ):
        """
        Adds a project to the data-provider.

        Parameters:
            project (DebiAIProject): The instance of the DebiAIProject class.
        """
        project_metadata = extract_project_metadata(project)

        self.projects.append(
            ProjectToExpose(
                project=project,
                project_name=project_metadata["name"],
            )
        )

    def get_projects(self) -> List[DebiAIProject]:
        """
        Get the list of projects.

        Returns:
            List[DebiAIProject]: The list of projects.
        """
        return [project.project for project in self.projects]

    def start_server(self, host="0.0.0.0", port=8000):
        # Print the server information
        console = Console()
        console.print(
            Panel(
                "The Data Provider is being started..."
                + f"\n\n[bold]API Server[/bold]: http://{host}:{port}"
                + f"\n[bold]Number of Projects[/bold]: {len(self.get_projects())}",
                title="DebiAI Data Provider",
                width=80,
                border_style="bold",
            )
        )

        # Print the details of each project
        for project in self.get_projects():
            console.print(project.get_details())

        start_api_server(self, host, port)
