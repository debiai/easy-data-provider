import os
import pandas as pd
import numpy as np
from debiai_data_provider.models.project import DebiAIProject
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table

# A Data-provider that only needs a path to a parquet file


class ParquetDataProviderConfig(BaseModel):
    parquet_path: str = Field(..., description="Path to the parquet file")
    sample_id_column_name: str = Field(
        ...,
        description="Name of the column containing the sample IDs, for the samples and results",
    )
    name: Optional[str] = Field(None, description="Name of the project")
    columns: Optional[List[str]] = Field(
        None, description="Columns to include in the project"
    )
    results_parquet_folder_path: Optional[str] = Field(  # Renamed field
        None, description="Path to the folder containing model results"
    )
    results_columns: Optional[List[str]] = Field(
        None, description="Columns for model results"
    )
    ignored_columns: Optional[List[str]] = Field(
        None, description="Columns to ignore in the project"
    )
    ignored_results_columns: Optional[List[str]] = Field(
        None, description="Columns to ignore in model results"
    )


class ParquetDataProvider(DebiAIProject):
    creation_date = "2025-03-28"
    # update_date = "2025-03-28"
    data: pd.DataFrame = None
    model_results: pd.DataFrame = None

    def __init__(
        self,
        parquet_path: str,
        sample_id_column_name: str,
        name: Optional[str] = None,
        columns: Optional[List[str]] = None,
        results_parquet_folder_path: Optional[str] = None,
        results_columns: Optional[List[str]] = None,
        ignored_columns: Optional[List[str]] = None,
        ignored_results_columns: Optional[List[str]] = None,
    ):
        super().__init__()
        self.config = ParquetDataProviderConfig(
            parquet_path=parquet_path,
            name=name,
            columns=columns,
            sample_id_column_name=sample_id_column_name,
            results_parquet_folder_path=results_parquet_folder_path,
            results_columns=results_columns,
            ignored_columns=ignored_columns,
            ignored_results_columns=ignored_results_columns,
        )

        # Setup name
        if self.config.name:
            self.name = self.config.name
        else:
            # Extract name from parquet_path
            self.name = Path(self.config.parquet_path).stem

        # Display project information
        console = Console()
        table = Table(title="Loading Parquet File")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        table.add_row("File Path", self.config.parquet_path)
        table.add_row("Project Name", self.name or "N/A")
        table.add_row(
            "Columns to Include",
            (
                "\n".join(f"  - {col}" for col in self.config.columns)
                if self.config.columns
                else "All"
            ),
        )
        table.add_row("Sample ID Column", self.config.sample_id_column_name)
        console.print(table)

        # Load the data from the parquet files
        self.load_project_parquet_samples()
        self.load_model_parquet_results()

    def load_project_parquet_samples(self):
        parquet_df = pd.read_parquet(self.config.parquet_path)

        # Check if the sample_id_column_name is in the columns
        if self.config.sample_id_column_name not in parquet_df.columns:
            console = Console()
            available_columns = "\n".join(f"  - {col}" for col in parquet_df.columns)
            console.print(
                f"[bold red]Error:[/bold red] Column '[cyan]{self.config.sample_id_column_name}[/cyan]'\
 not found in the parquet file.",
                style="red",
            )
            console.print(
                "[bold red]This column is required to identify the samples.[/bold red]",
                style="red",
            )
            console.print(
                f"[bold magenta]Available columns are:[/bold magenta]\n{available_columns}",
                style="magenta",
            )
            raise ValueError(
                f"Column '{self.config.sample_id_column_name}' not found in the parquet file."
            )

        # Check if all the sample IDs column values are type str
        for id in parquet_df[self.config.sample_id_column_name]:
            if not isinstance(id, str):
                console = Console()
                console.print(
                    "[bold red]Error:[/bold red] The sample IDs in the parquet file must be strings.",
                    style="red",
                )
                raise ValueError("Sample IDs must be strings.")

        # Check if the sample IDs are unique
        if not parquet_df[self.config.sample_id_column_name].is_unique:
            console = Console()
            console.print(
                "[bold red]Error:[/bold red] The sample IDs in the parquet file must be unique.",
                style="red",
            )
            raise ValueError("Sample IDs must be unique.")

        # Filter columns if specified
        if self.config.columns:
            columns_to_keep = set(self.config.columns)

            # Keep the sample_id_column_name if specified
            if self.config.sample_id_column_name:
                columns_to_keep.add(self.config.sample_id_column_name)

            parquet_df = parquet_df[list(columns_to_keep)]

        # Filter out ignored columns
        if self.config.ignored_columns:
            parquet_df = parquet_df.drop(
                columns=self.config.ignored_columns, errors="ignore"
            )

        # Validate data types and log faulty columns
        valid_types = (str, int, float, bool, list, dict)
        for column in parquet_df.columns:
            invalid_rows = parquet_df[column].apply(
                lambda x: not isinstance(x, valid_types)
            )
            if invalid_rows.any():
                # get whats the type of the first invalid value
                invalid_value_type = type(parquet_df[invalid_rows][column].iloc[0])

                console = Console()
                table = Table(
                    title=f"Invalid Data in Column '{column}'\nThis column might \
cause issues in DebiAI, you can use the `ignored_columns` parameter to ignore this column.",
                    show_header=True,
                    header_style="bold red",
                )
                table.add_column("Row Index", no_wrap=True)
                table.add_column("Value", style="red")
                table.add_row("Invalid Value Type", str(invalid_value_type))
                table.add_row("Invalid Rows Count", str(invalid_rows.sum()))

                for idx, value in parquet_df[invalid_rows][column].head(5).items():
                    table.add_row(str(idx), str(value))

                console.print(table)

        # Convert np.int64 to native Python int
        parquet_df = parquet_df.map(lambda x: int(x) if isinstance(x, np.int64) else x)

        # Store the data
        self.data = parquet_df

    def load_model_parquet_results(self):
        if not self.config.results_parquet_folder_path:
            return

        model_results = None

        for results_file in os.listdir(self.config.results_parquet_folder_path):
            if not results_file.endswith(".parquet"):
                continue

            model_name = results_file.split(".")[0]
            parquet_df = pd.read_parquet(
                os.path.join(self.config.results_parquet_folder_path, results_file)
            )

            # Check if the sample_id_column_name is in the columns
            if self.config.sample_id_column_name not in parquet_df.columns:
                console = Console()
                available_columns = "\n".join(
                    f"  - {col}" for col in parquet_df.columns
                )
                console.print(
                    f"[bold red]Error:[/bold red] Column \
'[cyan]{self.config.sample_id_column_name}[/cyan]' not found in the {model_name} parquet file.",
                    style="red",
                )
                console.print(
                    "[bold red]This column is required to map the model \
results to the samples.[/bold red]",
                    style="red",
                )
                console.print(
                    f"[bold magenta]Available columns are:[/bold magenta]\n{available_columns}",
                    style="magenta",
                )
                raise ValueError(
                    f"Column '{self.config.sample_id_column_name}' not found in the parquet file."
                )

            # Filter columns if specified
            if self.config.results_columns:
                columns_to_keep = set(self.config.results_columns)

                # Keep the sample_id_column_name if specified
                if self.config.sample_id_column_name:
                    columns_to_keep.add(self.config.sample_id_column_name)

                parquet_df = parquet_df[list(columns_to_keep)]

            # Filter out ignored columns
            if self.config.ignored_results_columns:
                parquet_df = parquet_df.drop(
                    columns=self.config.ignored_results_columns, errors="ignore"
                )

            # Add a _model_name column
            parquet_df["_model_name"] = model_name

            if model_results is None:
                model_results = parquet_df
            else:
                # Stack the results
                model_results = pd.concat(
                    [model_results, parquet_df], ignore_index=True
                )

        # Store the model results
        self.model_results = model_results

    # Project Info
    def get_structure(self) -> dict:
        # Load the data from the parquet file
        UNWANTED_COLUMNS = [self.config.sample_id_column_name]

        # Create the structure
        project_structure = {}

        for col in self.data.columns:
            if col in UNWANTED_COLUMNS:
                continue

            project_structure[col] = {
                "category": "context",
                "type": "auto",
            }

        return project_structure

    def get_results_structure(self) -> dict:
        # Load the data from the parquet file
        if not self.config.results_parquet_folder_path:
            raise NotImplementedError(
                "Results structure is not available for this project."
            )

        UNWANTED_COLUMNS = [self.config.sample_id_column_name]

        # Create the structure
        results_structure = {}

        # Iterate over the columns of the model_results DataFrame
        for col in self.model_results.columns:
            if col in UNWANTED_COLUMNS or col == "_model_name":
                continue

            results_structure[col] = {"type": "auto"}

        return results_structure

    # Project Samples
    def get_nb_samples(self) -> int:
        # This function returns the number of samples in the project
        return len(self.data)

    def get_samples_ids(self) -> List[str]:
        # This function returns the list of samples ids
        project_data = self.data
        return project_data[self.config.sample_id_column_name].tolist()

    def get_data(self, samples_ids: List[str]) -> pd.DataFrame:
        # This function will be called when the user
        # wants to analyze data from your project

        # The function should return a pandas DataFrame
        # containing the data corresponding to the samples_ids
        project_data = self.data.set_index(self.config.sample_id_column_name)
        data = project_data.loc[samples_ids]
        return data

    # Project models
    def get_models(self) -> List[dict]:
        # List the models available in the project
        if self.model_results is None:
            return []

        models = []
        # Get the list of models from model_results dataframe
        unique_model_names = self.model_results["_model_name"].unique()

        for model_name in unique_model_names:
            # Count the number of results for the model
            num_results = len(self.get_model_evaluated_data_id_list(model_name))

            models.append(
                {
                    "id": model_name,
                    "name": model_name,
                    "nb_results": num_results,
                }
            )

        # Sort the models by name
        models.sort(key=lambda x: x["name"])

        return models

    def get_model_evaluated_data_id_list(self, model_id: str) -> List[str]:
        # This function returns the list of sample IDs for a given model
        if not self.config.results_parquet_folder_path:
            return []

        # Filter the model results
        model_results = self.model_results[
            self.model_results["_model_name"] == model_id
        ]

        # Only keep the samples_id that are in the project data
        project_samples_id = self.get_samples_ids()
        model_results = model_results[
            model_results[self.config.sample_id_column_name].isin(project_samples_id)
        ]

        # Return the list of sample IDs
        return model_results[self.config.sample_id_column_name].tolist()

    def get_model_results(
        self, model_id: str, samples_ids: List[str]
    ) -> pd.DataFrame:  # noqa
        # Construct the path to the model's parquet file
        if not self.config.results_parquet_folder_path:
            return []

        # Filter the model results
        model_results = self.model_results[
            self.model_results["_model_name"] == model_id
        ]

        # Filter the results for the given sample IDs
        model_results = model_results[model_results["sample_id"].isin(samples_ids)]

        # Return the filtered DataFrame
        return model_results
