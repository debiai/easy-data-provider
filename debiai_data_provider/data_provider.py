from typing import List
from debiai_data_provider.utils.parser import extract_project_metadata
from debiai_data_provider.models.project import DebiAIProject, ProjectToExpose
from rich.console import Console
from rich.panel import Panel


class DataProvider:
    def __init__(self):
        self.projects: List[ProjectToExpose] = []

    def start_server(self, host="0.0.0.0", port=8000):
        from debiai_data_provider.app import start_api_server

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
        for project in self.projects:
            console.print(project.get_rich_table())

        start_api_server(self, host, port)

    # Projects
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

    def _get_project_to_expose(self, project_name: str) -> ProjectToExpose:
        """
        Get a project by its name.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            ProjectToExpose: The project to expose.
        """
        for project in self.projects:
            if project.project_name == project_name:
                return project

        raise ValueError(f"Project '{project_name}' not found.")
