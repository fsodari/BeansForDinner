from .recipe import Recipe
from . import atomic, collection, composite
import yaml
import os
import logging

# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

# Get base name of a file from the full path.
def file_basename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

# Returns a recipe instance based on the contents of a config dict.
def RecipeFactory(u_config):
    """ 
    Creates a class based on what kind of config was passed.
    This can accept a config dict or a list of recipes to be used to make a composite.
    If the config dict contains a 'source' field, the file will be read in and unpacked.
    If the recipe config contains a 'variants' field, this will return Collection(config)
    If the recipe config contains an 'ingredients' field, this will return Composite(config)
    """
    try:
        test_slice = u_config[:0]
        return composite.Composite(u_config)
    except TypeError:
        if not isinstance(u_config, dict):
            raise TypeError("Recipe Factory User Config must be a dict or a list!")

    config = u_config
    logging.info(f"User Config: {config}")
    # If a source file is provided, import the yaml file and use it as the config.
    # Any additional use config parameters are used as overrides.
    if 'source' in config.keys():
        config_file = config['source']
        filebasename = file_basename(config_file)
        # Read in yaml file.
        try:
            with open(config_file, 'r') as stream:
                config = yaml.safe_load(stream)
                # If the file is empty, create a default name.
                if config == None:
                    config = {'name':filebasename}

                # Apply any of the user overrides after the source is imported.
                config = Recipe.merge_config(config, u_config, merge_var=True, merge_ingr=True)
                logging.info(f"Recipe Factory Config: {config}")
        except FileNotFoundError:
            # If the file doesn't exist, create a new recipe using the file name.
            if 'name' not in config.keys():
                config['name'] = filebasename

    # A name is required for recipes created from a dict
    if 'name' not in config.keys():
        raise KeyError(f"Recipes must have a name! {config}")
    
    # Decide what recipe to create based on what is in the top level config.
    if 'variants' in config:
        return collection.Collection(config)
    # Composite implementation
    elif 'ingredients' in config:
        return composite.Composite(config)
    # Atomic implementation
    else:
        return atomic.Atomic(config)
        