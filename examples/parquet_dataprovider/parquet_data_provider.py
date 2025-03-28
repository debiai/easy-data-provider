import pandas as pd
import numpy as np
from debiai_data_provider import DebiAIProject, DataProvider

# This file presents an example of implementation for
# a parquet DebiAI Data-provider project.
# This Data-provider loads a parquet file and exposes it.

PARQUET_FILE_PATH = "ds.parquet"
PARQUET_ID_COLUMN = "sample_id"  # The column that contains the sample id


class ParquetDataProviderProject(DebiAIProject):
    creation_date = "2025-03-28"
    # update_date = "2025-03-28"
    data: pd.DataFrame = None

    def __init__(self):
        super().__init__()
        self.name = "Parquet Data project"
        self.get_project_parquet()

    def get_project_parquet(self):
        print("Loading data from parquet file")
        if self.data is not None:
            return self.data

        parquet_df = pd.read_parquet(PARQUET_FILE_PATH)

        # Convert np.int64 to native Python int
        data = parquet_df.map(
            lambda x: int(x) if isinstance(x, (np.integer)) else str(x)
        )

        self.data = data

    # Project Info
    def get_structure(self) -> dict:
        # Load the data from the parquet file
        UNWANTED_COLUMNS = [PARQUET_ID_COLUMN]

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

    # Project Samples
    def get_nb_samples(self) -> int:
        # This function returns the number of samples in the project
        return len(self.get_project_parquet())

    def get_samples_ids(self) -> list[str]:
        # This function returns the list of samples ids
        project_data = self.data
        return project_data[PARQUET_ID_COLUMN].tolist()

    def get_data(self, samples_ids: list[str]) -> pd.DataFrame:
        # This function will be called when the user
        # wants to analyze data from your project

        # The function should return a pandas DataFrame
        # containing the data corresponding to the samples_ids
        project_data = self.data.set_index(PARQUET_ID_COLUMN)
        data = project_data.loc[samples_ids]

        return data


provider = DataProvider()
provider.add_project(ParquetDataProviderProject())

# Finally, start the server
provider.start_server()
