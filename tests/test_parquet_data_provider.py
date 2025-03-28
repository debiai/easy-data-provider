import pandas as pd
from debiai_data_provider.providers.parquet_data_provider import ParquetDataProvider
from tests.test_utils import create_temp_parquet_file, create_temp_results_folder
import pytest


def test_bad_configurations():
    # Non-existing parquet_path
    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        ParquetDataProvider(
            parquet_path="non-existing", sample_id_column_name="sample_id"
        )

    data = pd.DataFrame(
        {
            "sample_id": ["1", "2", "3"],
            "class": ["A", "B", "C"],
            "value": [10, 20, 30],
        }
    )

    with create_temp_parquet_file(data) as parquet_path:
        # Non existing sample_id_column_name
        with pytest.raises(ValueError, match="Column 'non-existing' not found"):
            ParquetDataProvider(
                parquet_path=parquet_path, sample_id_column_name="non-existing"
            )

        # Results folder path does not exist
        with pytest.raises(
            FileNotFoundError, match="No such file or directory: 'non-existing'"
        ):
            ParquetDataProvider(
                parquet_path=parquet_path,
                sample_id_column_name="sample_id",
                results_csv_folder_path="non-existing",
            )
        # Results folder path is not a directory
        with pytest.raises(NotADirectoryError, match="Not a directory"):
            ParquetDataProvider(
                parquet_path=parquet_path,
                sample_id_column_name="sample_id",
                results_csv_folder_path=parquet_path,
            )

    # Samples IDs must be strings
    data = pd.DataFrame(
        {
            "sample_id": [1, 2, 3],
            "class": ["A", "B", "C"],
            "value": [10, 20, 30],
        }
    )
    with create_temp_parquet_file(data) as parquet_path:
        with pytest.raises(ValueError, match="Sample IDs must be strings"):
            ParquetDataProvider(
                parquet_path=parquet_path, sample_id_column_name="sample_id"
            )

    # Sample IDs must be unique
    data = pd.DataFrame(
        {
            "sample_id": ["1", "2", "1"],
            "class": ["A", "B", "C"],
            "value": [10, 20, 30],
        }
    )
    with create_temp_parquet_file(data) as parquet_path:
        with pytest.raises(ValueError, match="Sample IDs must be unique"):
            ParquetDataProvider(
                parquet_path=parquet_path, sample_id_column_name="sample_id"
            )

    # results with non-existing sample_id


def test_parquet_data_provider_basic():
    # Create a temporary parquet file
    data = pd.DataFrame(
        {
            "sample_id": ["s1", "s2", "s3"],
            "class": ["A", "B", "C"],
            "value": [10, 20, 30],
        }
    )
    with create_temp_parquet_file(data) as parquet_path:
        provider = ParquetDataProvider(
            parquet_path=parquet_path,
            sample_id_column_name="sample_id",
        )

        # Test get_nb_samples
        assert provider.get_nb_samples() == 3

        # Test get_samples_ids
        assert provider.get_samples_ids() == ["s1", "s2", "s3"]

        # Test get_data
        returned_data = provider.get_data(["s1", "s2"])
        assert returned_data.index.tolist() == ["s1", "s2"]
        assert returned_data["class"].tolist() == ["A", "B"]
        assert returned_data["value"].tolist() == [10, 20]

        # Test custom name
        provider = ParquetDataProvider(
            parquet_path=parquet_path,
            sample_id_column_name="sample_id",
            name="test_name",
        )
        assert provider.name == "test_name"


def test_parquet_data_provider_with_results():
    # Create a temporary parquet file
    data = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3"],
            "class": ["A", "B", "C"],
            "value": [10, 20, 30],
        }
    )
    results = {
        "m1": pd.DataFrame(
            {
                "sample_id": ["S1", "S2"],
                "predicted_state": ["OK", "KO"],
                "score": [0.9, 0.8],
            }
        ),
        "m2": pd.DataFrame(
            {
                "sample_id": ["S2", "S3"],
                "predicted_state": ["KO", "OK"],
                "score": [0.7, 0.6],
            }
        ),
    }
    with create_temp_parquet_file(data) as parquet_path, create_temp_results_folder(
        results
    ) as results_dir:
        provider = ParquetDataProvider(
            parquet_path=parquet_path,
            sample_id_column_name="sample_id",
            results_csv_folder_path=results_dir,
        )

        # Test get_models
        models = provider.get_models()
        assert len(models) == 2
        assert models[0]["id"] == "m1"
        assert models[0]["name"] == "m1"
        assert models[1]["id"] == "m2"
        assert models[1]["name"] == "m2"

        # Test get_model_evaluated_data_id_list
        assert provider.get_model_evaluated_data_id_list("m1") == ["S1", "S2"]
        assert provider.get_model_evaluated_data_id_list("m2") == ["S2", "S3"]

        # Test get_model_results
        m1_results = provider.get_model_results("m1", ["S1", "S2"])
        assert m1_results["sample_id"].tolist() == ["S1", "S2"]
        assert m1_results["predicted_state"].tolist() == ["OK", "KO"]
        assert m1_results["score"].tolist() == [0.9, 0.8]

        m2_results = provider.get_model_results("m2", ["S2", "S3"])
        assert m2_results["sample_id"].tolist() == ["S2", "S3"]
        assert m2_results["predicted_state"].tolist() == ["KO", "OK"]
        assert m2_results["score"].tolist() == [0.7, 0.6]


def test_parquet_data_provider_with_columns():
    # Create a temporary parquet file
    data = pd.DataFrame(
        {
            "sample_id": ["1", "2", "3"],
            "class": ["A", "B", "C"],
            "value": [10, 20, 30],
        }
    )
    with create_temp_parquet_file(data) as parquet_path:
        provider = ParquetDataProvider(
            parquet_path=parquet_path,
            sample_id_column_name="sample_id",
            columns=["class"],
        )

        # Test get_data with filtered columns
        data = provider.get_data(["1", "2"])
        assert data.index.tolist() == ["1", "2"]
        assert "class" in data.columns
        assert "value" not in data.columns
        assert data["class"].tolist() == ["A", "B"]
