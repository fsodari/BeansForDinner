import yaml
from .recipe import Recipe
from .recipe import rcp_cfg
import os
import logging
# rcpf_logger = logging.getLogger('RecipeFactoryLogger')
# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

class RecipeFactory:
    def __init__(self, logger):
        self.logger = logger

    @classmethod
    def rcp_file_basename(cls, filepath):
        return os.path.splitext(os.path.basename(filepath))[0]

    def get(self, config:dict):
        # TODO: If a list was supplied, each element needs a RecipeFactory.
        # If no source is supplied, an atomic will be used
        if 'source' in config.keys():
            config_file = config['source']
            filebasename = RecipeFactory.rcp_file_basename(config_file)
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
        
        self.logger.info(f"Recipe Factory: {config['name']}")

        # Collections implementation. Returns a lambda that accepts arguments.
        if 'variants' in config:
            return self.collection_factory(config)
        # Composite implementation
        elif 'ingredients' in config:
            return self.composite_factory(config)
        # Atomic implementation
        else:
            return self.atomic_factory(config)
        
    ###
    # Atomics
    ###

    # Atomic recipe factory. Atomic recipes have no ingredients.
    def atomic_factory(self, config:dict={}):
        # Allow higher-level recipes to override lower level recipe attributes.
        def atomic_init(rcpself:Recipe, config:dict={}):
            self.logger.info(f"Atomic Overrides: {config}")
            # Always initialize the base class
            Recipe.__init__(rcpself)
            # Override attrs using ones provided in the config.
            over_cfg = {**getattr(rcpself, rcp_cfg), **config}
            setattr(rcpself, rcp_cfg, over_cfg)
            self.logger.info(f"Atomic Final: {over_cfg}\n")
            
        # Default configuration.
        self.logger.info(f"Atomic Factory: {config}")
        class_config = {'__init__':atomic_init, rcp_cfg:config}
        return type(config['name'], (Recipe,), class_config)

    ###
    # Composites
    ###

    # Composites can contain multiple recipes as ingredients. The default ingredients
    # can be overriden with arguments in the constructor.
    def composite_factory(self, config:dict):
        # Params is a dict of recipe config dicts. If the param override matches, replace it.
        def composite_init(rcpself:Recipe, config:dict={}):
            self.logger.info(f"Composite Overrides: {config}")
            # Always initialize the base class
            Recipe.__init__(rcpself)
            # Override default ingredients
            temp_cfg = getattr(rcpself, rcp_cfg)
            if 'ingredients' in config:
                for k in config['ingredients']:
                    temp_cfg['ingredients'][k] = config['ingredients'][k]
            
            # Create ingredients.
            for k in temp_cfg['ingredients']:
                print(temp_cfg['ingredients'][k])
                ingr_rcp = [self.get(x)(x) for x in temp_cfg['ingredients'][k]]
                # Override the config with a recipe class. What are types even really?
                temp_cfg['ingredients'][k] = ingr_rcp

            self.logger.info(f"Composite Final: {temp_cfg}")
            setattr(rcpself, rcp_cfg, temp_cfg)

        # Default configuration.
        self.logger.info(f"Composite Factory: {config}")
        class_config = {'__init__':composite_init, rcp_cfg:config}
        return type(config['name'], (Recipe,), class_config)

    ###
    # Collections
    ###

    # Collections contain a dict of recipes and recipe overrides.
    # Choose which recipe you want to use at object creation time. 
    def collection_factory(self, config:dict):
        # When overriding collections, it will choose the variant, then apply overrides.
        def collection_new(cls:Recipe, config:dict={}):
            self.logger.info(f"Collection Overrides: {config}")
            # Overrides, including 'which'
            temp_cfg = getattr(cls, rcp_cfg)
            if 'variants' in config:
                for k in config['variants']:
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
            print(recipe_choice)
            choice = [self.get(x)(x) for x in recipe_choice]
            for rcp_ in recipe_choice:
                self.logger.info(f"Collection Final: {rcp_}")
            return choice

        self.logger.info(f"Collection Default: {config}")
        class_config = {'__new__': collection_new, rcp_cfg:config}
        return type(config['name'], (Recipe,), class_config)

# Generic recipe factory creator. This will parse the config file
# and figure out which category it is based on the config file.