import yaml
from .recipe import Recipe
import os
import logging
# rcpf_logger = logging.getLogger('RecipeFactoryLogger')
# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

def rcp_file_basename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

# Atomic recipe factory. Atomic recipes have no ingredients.
# def atomic_factory(config:dict={}):
    # Default configuration.
    # class_config = {'rcp': config}
    # logging.info(f"Atomic Factory: {config['name']}, Config: {config}")

    # return type(config['name'], (Atomic,), class_config)
    # return Atomic(config)

# Composites can contain multiple recipes as ingredients. The default ingredients
# can be overriden with arguments in the constructor.
# def composite_factory(config:dict={}):
    # Default configuration.
    # class_config = {'rcp':config}
    # logging.info(f"Composite Factory: {config['name']}, Config: {config}")
    # return type(config['name'], (Composite,), class_config)
    # return Composite(config)

# Collections contain a dict of recipes and recipe overrides.
# Choose which recipe you want to use at object creation time. 
# def collection_factory(config:dict={}):
    # class_config = {'rcp':config}
    # logging.info(f"Collection Factory: {config['name']}, Config: {config}")
    # return type(config['name'], (Collection,), class_config)
    # return Collection(config)
    
def RecipeFactory(u_config:dict):
    # TODO: If a list was supplied, interpret it as a
    # If no source is supplied, an atomic will be used
    config = u_config
    if 'source' in u_config.keys():
        config_file = u_config['source']
        filebasename = rcp_file_basename(config_file)
        # Read in yaml file.
        try:
            with open(config_file, 'r') as stream:
                config = yaml.safe_load(stream)
                if config == None:
                    config = {'name':filebasename}
                # Keep overrides.
                logging.info(f"RF User Config: {u_config}")
                # config = {**config, **old_cfg}
                # config = config | old_cfg
                config = Recipe.merge_config(config, u_config, merge_var=True, merge_ingr=True)
                logging.info(f"RF New Config: {config}")
        except FileNotFoundError:
            # If the file doesn't exist, create a new atomic recipe using the file name.
            if 'name' not in u_config.keys():
                config = {'name':filebasename}

    # A name is required for recipes created from a dict
    if 'name' not in config.keys():
        raise KeyError(f"Recipes must have a name! {config}")
    
    logging.info(f"Recipe Factory: {config['name']}")

    # Fix this or nah?
    from .atomic import Atomic
    from .collection import Collection
    from .composite import Composite
    # Collections implementation. Returns a lambda that accepts arguments.
    if 'variants' in config:
        return Collection(config)
    # Composite implementation
    elif 'ingredients' in config:
        return Composite(config)
    # Atomic implementation
    else:
        return Atomic(config)
        