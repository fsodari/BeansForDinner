import yaml
from Recipe import Recipe, recipe
from Recipe import SteelCutOats
import yaml
# Create a class dynamically using:
# Class = type('ClassName', (Recipe,), {'__init__': __init__, 'printX': printX})

# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

# Generic init function containing all required members.
# Use a higher order function to wrap this
def rcpf_init(self:Recipe, params:dict):
    pass

def rcpf_name(self:Recipe, name:str) -> str:
    return name

def rcpf_cooking_time(self: Recipe, cooking_time:float) -> float:
    return cooking_time

# Populate/update methods if they exist. easy.
def get_main_methods(config:dict, methods:dict) -> dict:
    if 'name' in config:
        methods['name'] = lambda self: rcpf_name(self, config['name'])
    if 'cooking_time' in config:
        methods['cooking_time'] = lambda self: rcpf_cooking_time(self, config['cooking_time'])
    return methods
# Set defaults
def override_main_methods(self:Recipe, config:dict):
    if 'name' in config:
        setattr(self, 'name', lambda self: rcpf_name(self, config['name']))
    if 'cooking_time' in config:
        setattr(self, 'cooking_time', lambda self: rcpf_cooking_time(self, config['cooking_time']))

# Atomic recipe factory
def AtomicRecipeFactory(config:dict):
    methods = get_main_methods(config, {})
    return type(config['name'], (Recipe,), methods)

def collection_new(cls:Recipe, variants:dict, which:str):
    # Enforce a default option in collections.
    if which is None:
        which = next(iter(variants))
    
    recipe_choice = variants[which]
    inst = RecipeFactory(recipe_choice['source'])
    # Apply collection overrides
    override_main_methods(inst, recipe_choice)
    return inst()

# Collection Factory.
def CollectionFactory(config:dict):
    # Find source of the specific recipe we will implement
    variants = config['variants']
    methods = get_main_methods(config, {})
    methods['__new__'] = lambda cls, which=None: collection_new(cls, variants, which)
    return type(config['name'], (Recipe,), methods)

# Params is a dict of class definitions
# Need to get instances of all classes.
def composite_init(self:Recipe, defaults:dict, params:dict={}):
    # Override defaults
    for p in params:
        if p in defaults:
            defaults[p] = params[p]
    # Update the ingredients member to have instances of all classes.
    self.ingredients = {k:defaults[k] for k in defaults}

# params is a dict of classes.
def CompositeRecipeFactory(config:dict):
    methods = get_main_methods(config, {})
    # Add default classes.
    defaults = {k:RecipeFactory(config['ingredients'][k]['source'])() for k in config['ingredients']}

    # Init method takes optional parameters
    methods['__init__'] = lambda self, params={}: composite_init(self, defaults, params)
    # methods['ingredients'] = lambda self: 
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
        
if __name__ == '__main__':
    # Atomic recipe example
    # Get a new recipe factory from a yaml template. Neat.
    steel_class = RecipeFactory('recipe_config/SteelCutOats.yml')
    # Get an instance of the recipe
    steel_inst = steel_class()
    
    print(f"Default SteelCutOats: Name: {steel_inst.name()}, Cooking Time: {steel_inst.cooking_time()}")

    # Collection example.
    oats_coll = RecipeFactory('recipe_config/Oats.yml')
    # Get instances of the class.
    oats_inst = oats_coll() # Default option
    oats_inst2 = oats_coll('RolledOats')
    print(f"Oats Collection SCO Name: {oats_inst.name()}, Cooking Time: {oats_inst.cooking_time()}")
    print(f"Oats Collection Rolled Name: {oats_inst2.name()}, Cooking Time: {oats_inst2.cooking_time()}")

    # Composite Recipe example
    oatmeal_comp = RecipeFactory('recipe_config/Oatmeal.yml')
    # Using default arguments
    oatmeal_inst = oatmeal_comp()
    print(f"Oatmeal: Name: {oatmeal_inst.name()}")
    print(f"Oatmeal Base: {oatmeal_inst.ingredients['base'].name()}, Liquid: {oatmeal_inst.ingredients['liquid'].name()}")

    # Use a different ingredient from the oats collection
    oatmeal_inst2 = oatmeal_comp({'base':oats_coll('RolledOats')})

    print(f"Oatmeal2 Base: {oatmeal_inst2.ingredients['base'].name()}, Liquid: {oatmeal_inst2.ingredients['liquid'].name()}")
    # This could be implemented in the base class
    total_cook_time = 0
    for i in oatmeal_inst.ingredients:
        total_cook_time += oatmeal_inst.ingredients[i].cooking_time()
    print(f"Total Cook Time: {total_cook_time}")
