from typing import List
from debiai_data_provider.utils.parser import extract_project_class_name
from debiai_data_provider.models.project import DebiAIProject, ProjectToExpose
from debiai_data_provider.version import VERSION
from rich.console import Console
from rich.panel import Panel


class DataProvider:
    def __init__(
        self,
        max_sample_id_by_request=10000,
        max_sample_data_by_request=2000,
        max_result_by_request=5000,
    ):
        """
        Initializes the DataProvider with optional parameters for maximum limits.

        Parameters:
            max_sample_id_by_request (int): Maximum number of sample IDs in a single request.
            max_sample_data_by_request (int): Maximum number of sample data in a single request.
            max_result_by_request (int): Maximum number of results in a single request.
        """
        self.projects: List[ProjectToExpose] = []
        self.max_sample_id_by_request = max_sample_id_by_request
        self.max_sample_data_by_request = max_sample_data_by_request
        self.max_result_by_request = max_result_by_request

    def start_server(self, host="0.0.0.0", port=8000):
        from debiai_data_provider.app import start_api_server

        # Print the server information
        console = Console()
        panel_text = (
            "The Data Provider is being started..."
            + f"\n\n[bold]API Server[/bold]: http://{host}:{port}"
            + f"\n[bold]Number of Projects[/bold]: {len(self.get_projects())}"
        )

        # Display parameters
        panel_text += "\n[bold]Parameters[/bold]:\n  " + "\n  ".join(
            [
                f"Max sample id by request: {self.max_sample_id_by_request}",
                f"Max sample data by request: {self.max_sample_data_by_request}",
                f"Max result by request: {self.max_result_by_request}",
            ]
        )

        console.print(
            Panel(
                panel_text,
                title=f"DebiAI Data Provider v{VERSION}",
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
        if project.name:
            project_name = project.name
        else:
            project_name = extract_project_class_name(project)

        # Check if the project name already exists
        for existing_project in self.projects:
            if existing_project.project_name == project_name:
                raise ValueError(
                    f"A project with the name '{project_name}' already exists."
                )

        self.projects.append(
            ProjectToExpose(
                project=project,
                project_name=project_name,
            )
        )

    def get_projects(self) -> List[DebiAIProject]:
        """
        Get the list of projects.

        Returns:
            List[DebiAIProject]: The list of projects.
        """
        return [project.project for project in self.projects]

    def get_project(self, project_name: str) -> DebiAIProject:
        """
        Get a project by its name.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            DebiAIProject: The project.
        """
        return self._get_project_to_expose(project_name).project

    def delete_project(self, project_name: str):
        """
        Deletes a project from the data-provider.

        Parameters:
            project_name (str): The name of the project to delete.
        """
        project_to_delete = self.get_project(project_name)
        try:
            project_to_delete.delete_project()
            self.projects = [
                project
                for project in self.projects
                if project.project_name != project_name
            ]
        except NotImplementedError:
            print(
                f"Project '{project_name}' does not implement the delete_project method."
            )

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
