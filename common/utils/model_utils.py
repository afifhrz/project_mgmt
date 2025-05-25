import json
from django.forms import model_to_dict

def add_json_to_model(models):
    """
    Add json form in the given models.
    """
    for model in models:
        model.json_data = json.dumps(model_to_dict(model), indent=4, sort_keys=True, default=str)  # Convert to JSON string
    return models

def prettify_field(field):
    return ' '.join(word.capitalize() for word in field.split('_'))