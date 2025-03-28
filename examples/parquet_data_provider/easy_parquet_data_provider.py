from debiai_data_provider import DataProvider, ParquetDataProvider

provider = DataProvider()
provider.add_project(
    ParquetDataProvider(
        parquet_path="examples/parquet_data_provider/ds.parquet",
        sample_id_column_name="sample_id",
        ignored_columns=["sha256", "resolution"],
    )
)
provider.start_server()
