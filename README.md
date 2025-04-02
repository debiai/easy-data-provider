# DebiAI Data Provider Python module

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This [DebiAI](https://debiai.irt-systemx.fr/) Data Provider Python module allows you to easily deploy your own data-provider through the data-provider API.

A data-provider allows you to provide data to DebiAI so that no duplication of data is needed.

[DebiAI Data-providers documentation](https://debiai.irt-systemx.fr/dataInsertion/dataProviders/)

## Getting started

### Installation

Install `debiai_data_provider` with pip:

```bash
pip install debiai_data_provider
```

### Usage

Create a new Python file, for example `my_data_provider.py` and copy the content of the [simple_project.py](examples/simple_project.py) Data-provider.

Run the Python file and your project is now available through the DebiAI Data Provider API!

This way of creating a data-provider is the most generic one, you can customize it to support any data-sources.

We also provide a higher level of abstraction to create data-providers:

- [ParquetDataProvider](debiai_data_provider/parquet_data_provider.py) is a data-provider that provides data from a parquet file. It is a simple way to create a data-provider with a parquet file as input.

#### Plug-in your data-provider with DebiAI

To link your data-provider with DebiAI, you can follow our [Creation of a data provider guide](https://debiai.irt-systemx.fr/dataInsertion/dataProviders/quickStart.html)

### Examples

Find out how to use the DebiAI Data Provider Python module in the [examples](examples) folder:

#### Generic Data-providers

- [simple_project.py](examples/simple_project.py) shows how to create a simple data-provider with a project
- [project_with_results.py](examples/project_with_results.py) shows how to create a data-provider with a project that also provides model results
- [parquet_data_provider.py](examples/parquet_data_provider/parquet_data_provider.py) shows how to create a data-provider that provides data from a parquet file

#### Data-providers with a higher level of abstraction

- [easy_parquet_data_provider.py](examples/parquet_data_provider/easy_parquet_data_provider.py) does the same as the previous example but with a higher implementation level, using the `ParquetDataProvider` class.

## Testing

To run the tests, install the dependencies and run the tests with `pytest`:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
python -m pytest --cov=debiai_data_provider
```

Tested versions:

- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

## Roadmap

- [x] Publish to Pypi
- [ ] Provide project data
  - [x] Provide project metadata
  - [x] Provide project samples
  - [x] Provide project models & model results
  - [ ] Provide project selections
- [ ] Make available project interactions
  - [x] Project deletion
  - [ ] Model deletion
  - [ ] Selection creation
  - [ ] Selection deletion
- [ ] High level data-providers
  - [ ] CSV data-provider
  - [ ] Json data-provider
- [ ] Start DebiAI along with the data-provider
- [ ] Create a welcome page that shows the data-provider status and projects
- [ ] LLM improved data-provider for auto configuration

---

<p align="center">
  DebiAI is developed by 
  <a href="https://www.irt-systemx.fr/" title="IRT SystemX">
   <img src="https://www.irt-systemx.fr/wp-content/uploads/2013/03/system-x-logo.jpeg"  height="70">
  </a>
  And is integrated in 
  <a href="https://www.confiance.ai/" title="Confiance.ai">
   <img src="https://pbs.twimg.com/profile_images/1443838558549258264/EvWlv1Vq_400x400.jpg"  height="70">
  </a>
</p>

---
