import os
from tempfile import TemporaryDirectory
from contextlib import contextmanager


@contextmanager
def create_temp_parquet_file(dataframe):
    """
    Context manager to create a temporary parquet file from a given DataFrame.
    Automatically cleans up the temporary file on exit.
    """
    with TemporaryDirectory() as temp_dir:
        data_path = os.path.join(temp_dir, "data.parquet")
        dataframe.to_parquet(data_path)
        yield data_path


@contextmanager
def create_temp_results_folder(results_dict):
    """
    Context manager to create a temporary folder with multiple parquet files for model results.
    Automatically cleans up the temporary folder on exit.
    """
    with TemporaryDirectory() as temp_dir:
        for model_name, dataframe in results_dict.items():
            model_path = os.path.join(temp_dir, f"{model_name}.parquet")
            dataframe.to_parquet(model_path)
        yield temp_dir
