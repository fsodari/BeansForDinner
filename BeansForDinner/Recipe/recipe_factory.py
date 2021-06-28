import yaml
from .recipe import Recipe
import os

# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

# This is where all of the config setttings are stored in each class.
rcp_cfg_atr = 'rcp_config'

def rcp_file_basename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

# Allow higher-level recipes to override lower level recipe attributes.
def atomic_init(self:Recipe, config:dict={}):
    print(config)
    # Override attrs using ones provided in the config.
    temp_cfg = getattr(self, rcp_cfg_atr)
    for k in config:
        temp_cfg[k] = config[k]
    setattr(self, rcp_cfg_atr, temp_cfg)

# Atomic recipe factory. Atomic recipes have no ingredients.
def AtomicRecipeFactory(config:dict={}):
    class_config = {}
    class_config['__init__'] = atomic_init
    class_config[rcp_cfg_atr] = config

    return type(config['name'], (Recipe,), class_config)

# Params is a dict of recipe config dicts. If the param override matches, replace it.
def composite_init(self:Recipe, config:dict={}):
    temp_cfg = getattr(self, rcp_cfg_atr)
    # Initialize default ingredients.
    for k in temp_cfg['ingredients']:
        # Override the configuration with a class
        ingr_rcp = RecipeFactory(temp_cfg['ingredients'][k])
        temp_cfg['ingredients'][k] = ingr_rcp

    # Override ingredients.
    if 'ingredients' in config:
        for k in config['ingredients']:
            ingr_rcp = RecipeFactory(config['ingredients'][k])
            # Override the defaults
            temp_cfg['ingredients'][k] = ingr_rcp
    setattr(self, rcp_cfg_atr, temp_cfg)

# Composites can contain multiple recipes as ingredients. The default ingredients
# can be overriden with arguments in the constructor.
def CompositeRecipeFactory(config:dict):
    class_config = {}
    # Init method takes optional parameters
    class_config['__init__'] = composite_init
    class_config[rcp_cfg_atr] = config
    # methods['ingredients'] = lambda self: 
    return type(config['name'], (Recipe,), class_config)

def collection_new(cls:Recipe, variants:dict, config:dict={}):
    # Enforce a default option in collections.
    if 'which' not in config:
        which = next(iter(variants))
    else:
        which = config['which']
    
    # Decide what to do based on what which is...wait what?
    try:
        recipe_choice = variants[which]
    except TypeError as e:
        if type(which) is dict:
            recipe_choice = which
        else:
            raise TypeError('Collection overrides must use dicts')
    except KeyError as e:
        if type(which) is str:
            recipe_choice = {'name':which}
    # If source is not in the choice, create an atomic using the name.
    if 'source' not in recipe_choice.keys() and 'name' not in recipe_choice.keys():
        recipe_choice['name'] = which
    
    recipe_class = RecipeFactory(recipe_choice)
    return recipe_class(recipe_choice)

# Collections contain a dict of recipes and recipe overrides.
# Choose which recipe you want to use at object creation time. 
def CollectionFactory(config:dict):
    # Find source of the specific recipe we will implement
    variants = config['variants']
    class_config = {}
    class_config[rcp_cfg_atr] = config
    class_config['__new__'] = lambda cls, which={}: collection_new(cls, variants, which)
    return type(config['name'], (Recipe,), class_config)

# Generic recipe factory creator. This will parse the config file
# and figure out which category it is based on the config file.
def RecipeFactory(config:dict):
    # If no source is supplied, an atomic will be used
    if 'source' in config.keys():
        config_file = config['source']
        filebasename = rcp_file_basename(config_file)
        # Read in yaml file.
        try:
            with open(config_file, 'r') as stream:
                config = yaml.safe_load(stream)
                if config == None:
                    config = {'name':filebasename}
        except FileNotFoundError:
            # If the file doesn't exist, create a new atomic recipe using the file name.
            if 'name' not in config.keys():
                config = {'name':filebasename}

    # A name is required for recipes created from a dict
    if 'name' not in config.keys():
        raise KeyError(f"Recipes must have a name!")
    # Collections implementation. Returns a lambda that accepts arguments.
    if 'variants' in config:
        return CollectionFactory(config)
    # Composite implementation
    elif 'ingredients' in config:
        return CompositeRecipeFactory(config)
    # Atomic implementation
    else:
        return AtomicRecipeFactory(config)
        