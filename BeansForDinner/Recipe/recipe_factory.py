import yaml
from .recipe import Recipe
import yaml
# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

# These are the generic base methods that will be used to generate new methods based on the recipe config.
def rcpf_name(self:Recipe, name:str) -> str:
    return name

def rcpf_cooking_time(self: Recipe, cooking_time:float) -> float:
    return cooking_time

# Populate/update methods if they exist in the config file.
def get_main_methods(config:dict, methods:dict) -> dict:
    if 'name' in config:
        methods['name'] = lambda self: rcpf_name(self, config['name'])
    if 'cooking_time' in config:
        methods['cooking_time'] = lambda self: rcpf_cooking_time(self, config['cooking_time'])
    return methods

# Allow higher-level recipes to override lower level recipes.
def override_main_methods(self:Recipe, config:dict):
    if 'name' in config:
        setattr(self, 'name', lambda self: rcpf_name(self, config['name']))
    if 'cooking_time' in config:
        setattr(self, 'cooking_time', lambda self: rcpf_cooking_time(self, config['cooking_time']))

# Atomic recipe factory. Atomic recipes accept no ingredients as construction parameters.
# TODO: Atomics may not contain ingredients, but their methods can be overriden.
def AtomicRecipeFactory(config:dict):
    methods = get_main_methods(config, {})
    return type(config['name'], (Recipe,), methods)


# Composites can contain multiple recipes as ingredients. The default ingredients
# can be overriden with arguments in the constructor.
def CompositeRecipeFactory(config:dict):
    # Params is a dict of class definitions. If the param override matches, replace it.
    def composite_init(self:Recipe, defaults:dict, params:dict={}):
        # Override defaults
        for p in params:
            if p in defaults:
                defaults[p] = params[p]
        # Update the ingredients member to have instances of all classes.
        self.ingredients = {k:defaults[k] for k in defaults}
    
    methods = get_main_methods(config, {})
    # Add default classes.
    defaults = {k:RecipeFactory(config['ingredients'][k]['source'])() for k in config['ingredients']}

    # Init method takes optional parameters
    methods['__init__'] = lambda self, params={}: composite_init(self, defaults, params)
    # methods['ingredients'] = lambda self: 
    return type(config['name'], (Recipe,), methods)

# Collections contain a dict of recipes and recipe overrides.
# Choose which recipe you want to use at object creation time. 
def CollectionFactory(config:dict):
    def collection_new(cls:Recipe, variants:dict, which:str):
        # Enforce a default option in collections.
        if which is None:
            which = next(iter(variants))
        
        recipe_choice = variants[which]
        inst = RecipeFactory(recipe_choice['source'])
        # Apply collection overrides
        override_main_methods(inst, recipe_choice)
        return inst()

    # Find source of the specific recipe we will implement
    variants = config['variants']
    methods = get_main_methods(config, {})
    methods['__new__'] = lambda cls, which=None: collection_new(cls, variants, which)
    return type(config['name'], (Recipe,), methods)

# Generic recipe factory creator. This will parse the config file
# and figure out which category it is based on the config file.
def RecipeFactory(config_file:str):
    # Read in yaml file.
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    # Collections implementation. Returns a lambda that accepts arguments.
    if 'variants' in config:
        return CollectionFactory(config)
    # Composite implementation
    elif 'ingredients' in config:
        return CompositeRecipeFactory(config)
    # Atomic implementation
    else:
        return AtomicRecipeFactory(config)
        