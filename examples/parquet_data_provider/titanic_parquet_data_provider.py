from debiai_data_provider import DataProvider, ParquetDataProvider

provider = DataProvider()
provider.add_project(
    ParquetDataProvider(
        parquet_path="examples/parquet_data_provider/id_titanic.parquet",
        sample_id_column_name="PassengerId",
        ignored_columns=["Cabin", "Embarked", "Fare", "Pclass", "Survived", "Age",
                         "SibSp", "Parch", "Ticket"],
    )
)
provider.start_server(port=8082)
