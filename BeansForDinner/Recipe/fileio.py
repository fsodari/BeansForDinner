import os
from typing import OrderedDict
import yaml
    
def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

def sort_recipe_config(config:dict) -> dict:
    """
    When exporting a recipe, sort the fields so that name and source are at the top.
    This will make the recipe outputs look more consistent.
    """
    print(config.keys())
    return config

def file_basename(filepath):
    """Get base name of a file from the full path."""
    return os.path.splitext(os.path.basename(filepath))[0]

def import_recipe(config_file:str) -> dict:
    """
    Given a path to a yaml file, read in the file as a dict.
    If the file does not exist, an empty recipe is created using the file basename.
    """
    config = {}
    filebasename = file_basename(config_file)
    # Read in yaml file.
    try:
        with open(config_file, 'r') as stream:
            config = yaml.safe_load(stream)
            # If the file is empty, create a default name.
            if config == None:
                config = {'name':filebasename}

    except FileNotFoundError:
        # If the file doesn't exist, create a new recipe using the file name.
        config['name'] = filebasename

    return config

def export_recipe(config:dict, config_file:str) -> None:
    """Save a configuration dict as a yaml file."""
    with open(config_file, 'w') as stream:
        yaml.dump(config, stream, sort_keys=False)
