# DebiAI Data Provider Python module

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This DebiAI Data Provider Python module allows you to easily deploy your own data-provider through the data-provider API.

A data-provider allows you to provide data to DebiAI so that no duplication of data is needed.

[DebiAI Data-providers documentation](https://debiai.irt-systemx.fr/dataInsertion/dataProviders/)

## Getting started

Install `debiai_data_provider` with pip:

```bash
pip install debiai_data_provider
```

Then, create a Python Class representing your project:

```python
from debiai_data_provider import DebiAIProject, DataProvider


class MyProject(DebiAIProject):
    creation_date = "2024-01-01"

    def get_structure(self) -> dict:
        # This function will be called when the user
        # opens the project in the DebiAI interface
        # It serves to classify the project data structure

        return {
            "Data ID": {"type": "text", "category": "id"},
            "My context 1": {"type": "text", "category": "context"},
            "My context 2": {"type": "number", "category": "context"},
            "My groundtruth 1": {"type": "number", "category": "groundtruth"},
        }

    def get_data(self) -> pd.DataFrame:
        # This function will be called when the user
        # wants to analyze data from your project
        samples_df = pd.DataFrame(
            {
                "Data ID": ["image-1", "image-2", "image-3"],
                "My context 1": ["A", "B", "C"],
                "My context 2": [0.28, 0.388, 0.5],
                "My groundtruth 1": [8, 7, 19],
            }
        )

        return samples_df


my_project = MyProject()
```

Then, create an DataProvider object and add your project to it:

```python
provider = DataProvider()

provider.add_project(my_project)

# Finally, start the server
provider.start_server()
```

Run the Python file and your project is now available through the DebiAI Data Provider API!