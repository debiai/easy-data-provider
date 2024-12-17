from debiai_data_provider.models.project import DebiAIProject
from debiai_data_provider.models.debiai import Column
import pandas as pd
from typing import List


def extract_project_class_name(project: DebiAIProject) -> str:
    # Get the class name
    return project.__class__.__name__


def dataframe_to_debiai_data_array(
    columns: List[Column],
    samples_id: List[str],
    data: pd.DataFrame,
):
    sample_dicts = {}
    for sample_id in samples_id:
        sample_data = []

        for column in columns:
            try:
                if "Data ID" in data.columns:
                    sample_to_add = data.loc[
                        data["Data ID"] == sample_id, column.name
                    ].values[0]
                else:
                    # Use the dataframe index as the sample ID
                    sample_to_add = data.loc[sample_id, column.name]
            except KeyError:
                raise KeyError(
                    f"Column '{column.name}' of the sample '{sample_id}' not found in the data."
                )

            sample_data.append(sample_to_add)

        sample_dicts[sample_id] = sample_data

    return sample_dicts
