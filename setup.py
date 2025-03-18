from setuptools import setup, find_packages
from debiai_data_provider.version import VERSION

# Import the README and use it as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Setup the package
setup(
    name="debiai_data_provider",
    version=VERSION,
    description="Start your own Data-provider from simple Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/debiai/easy-data-provider",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pandas==2.2.3",
        "fastapi==0.115.4",
        "uvicorn==0.32.0",
        "rich==13.9.4",
    ],
    entry_points={},
)
