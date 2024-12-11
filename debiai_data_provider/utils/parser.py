from debiai_data_provider.models.project import DebiAIProject

TYPE_MAPPING = {
    "int": "number",
    "float": "number",
    "str": "string",
    "bool": "boolean",
    "list": "array",
    "Any": "any",
}


def extract_project_metadata(project: DebiAIProject) -> dict:
    # Get the class name
    class_name = project.__class__.__name__

    return {
        "name": class_name,
    }
