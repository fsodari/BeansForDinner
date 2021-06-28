import yaml
from .recipe import Recipe
from .recipe import rcp_cfg
import os

# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

def rcp_file_basename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

# Allow higher-level recipes to override lower level recipe attributes.
def atomic_init(self:Recipe, config:dict={}):
    # Always initialize the base class
    Recipe.__init__(self)
    # Override attrs using ones provided in the config.
    setattr(self, rcp_cfg, {**getattr(self, rcp_cfg), **config})

# Atomic recipe factory. Atomic recipes have no ingredients.
def AtomicRecipeFactory(config:dict={}):
    class_config = {'__init__':atomic_init, rcp_cfg:config}
    return type(config['name'], (Recipe,), class_config)

# Params is a dict of recipe config dicts. If the param override matches, replace it.
def composite_init(self:Recipe, config:dict={}):
    # Always initialize the base class
    Recipe.__init__(self)
    # Override default ingredients
    temp_cfg = getattr(self, rcp_cfg)
    if 'ingredients' in config:
        for k in config['ingredients']:
            if k in temp_cfg['ingredients']:
                temp_cfg['ingredients'][k] = {**temp_cfg['ingredients'][k], **config['ingredients'][k]}
            else:
                temp_cfg['ingredients'][k] = config['ingredients'][k]
    
    # Create ingredients.
    for k in temp_cfg['ingredients']:
        ingr_rcp = RecipeFactory(temp_cfg['ingredients'][k])
        # Override the config with a recipe class. What are types even really?
        temp_cfg['ingredients'][k] = ingr_rcp(temp_cfg['ingredients'][k])

    setattr(self, rcp_cfg, temp_cfg)

# Composites can contain multiple recipes as ingredients. The default ingredients
# can be overriden with arguments in the constructor.
def CompositeRecipeFactory(config:dict):
    class_config = {'__init__':composite_init, rcp_cfg:config}
    return type(config['name'], (Recipe,), class_config)

def collection_init(self:Recipe, config:dict={}):
    # Always initialize the base class.
    Recipe.__init__(self)
    # Overrides, including 'which'
    temp_cfg = getattr(self, rcp_cfg)
    if 'variants' in config:
        for k in config['variants']:
            if k in temp_cfg['variants']:
                temp_cfg['variants'][k] = {**temp_cfg['variants'][k], **config['variants'][k]}
            else:
                temp_cfg['variants'][k] = config['variants'][k]
    
    if 'which' in config:
        temp_cfg['which'] = config['which']
    # Enforce a default option in collections. Use first element.
    if 'which' not in temp_cfg:
        temp_cfg['which'] = next(iter(temp_cfg['variants']))

    # If the user override doesn't match anything, stick with the default.
    if temp_cfg['which'] not in temp_cfg['variants']:
        temp_cfg['which'] = next(iter(temp_cfg['variants']))
    
    # Create a new recipe using the choice
    recipe_choice = temp_cfg['variants'][temp_cfg['which']]
    choice = RecipeFactory(recipe_choice)(recipe_choice)

    # Replace collection config with choice config.
    setattr(self, rcp_cfg, getattr(choice, rcp_cfg))

# Collections contain a dict of recipes and recipe overrides.
# Choose which recipe you want to use at object creation time. 
def CollectionFactory(config:dict):
    class_config = {'__init__': collection_init, rcp_cfg:config}
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
        