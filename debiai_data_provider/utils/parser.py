from debiai_data_provider.models.project import DebiAIProject
from debiai_data_provider.models.debiai import Column
import pandas as pd
from typing import List


def extract_project_metadata(project: DebiAIProject) -> dict:
    # Get the class name
    class_name = project.__class__.__name__

    return {
        "name": class_name,
    }


def dataframe_to_debiai_data_array(
    columns: List[Column],
    samples_id: List[str],
    data: pd.DataFrame,
):
    sample_dicts = {}
    for sample_id in samples_id:
        sample_data = []

        for column in columns:
            sample_data.append(
                data.loc[data["Data ID"] == sample_id, column.name].values[0]
            )

        sample_dicts[sample_id] = sample_data

    return sample_dicts
