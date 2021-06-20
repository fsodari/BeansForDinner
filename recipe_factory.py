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

def rcpf_name(name:str) -> str:
    return name

def rcpf_cooking_time(cooking_time:float) -> float:
    return cooking_time

# Populate/update methods if they exist. easy.
def get_main_methods(config:dict, methods:dict) -> dict:
    if 'name' in config:
        methods['name'] = lambda self: rcpf_name(config['name'])
    if 'cooking_time' in config:
        methods['cooking_time'] = lambda self: rcpf_cooking_time(config['cooking_time'])
    return methods
    
# Generates a recipe from a collection and a selection.
def CollectionFactory(which:str, config:dict):
    # Find source of the specific recipe we will implement
    recipe_choice = config['variants'][which]
    # Create a new class from the source
    with open(recipe_choice['source'], 'r') as stream:
        sub_config = yaml.safe_load(stream)
    # Use methods for the class from the collection sub recipe defaults.
    class_name = sub_config['name']
    methods = get_main_methods(sub_config, {})
    # Now check if the collection recipe overrides anything. Again, need a better way.
    if 'name' in recipe_choice:
        class_name = recipe_choice['name']
    methods = get_main_methods(recipe_choice, methods)

    # Make a __new__ method that returns the correct recipe class
    return type(class_name, (Recipe,), methods)

def AtomicRecipeFactory(config:dict):
    methods = get_main_methods(config, {})
    return type(config['name'], (Recipe,), methods)

# Params is a dict of class definitions
def composite_init(self:Recipe, params:dict):
    self.params = params

def CompositeRecipeFactory(config:dict, params:dict={}):
    methods = get_main_methods(config, {})
    methods['__init__'] = lambda self, params: composite_init(self, params)

    # Need to build all the ingredients classes.
    ingr = config['ingredients']
    pass


def RecipeFactory(config_file:str):
    # Read in yaml file.
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    # Collections implementation.
    if 'variants' in config:
        return lambda which: CollectionFactory(which, config)
    # Composite implementation
    elif 'ingredients' in config:
        return lambda params: CompositeRecipeFactory(params, config)
    # Atomic implementation
    else:
        return lambda: AtomicRecipeFactory(config)
        
if __name__ == '__main__':
    # Get a new recipe factory from a yaml template. Neat.
    sco_rcp = RecipeFactory('recipe_config/SteelCutOats.yml')
    # Get a recipe from the factory
    rcp_class = sco_rcp()
    # Get an instance of the recipe
    rcp_inst = rcp_class()

    # Use a collection to get an instance.
    # Load the collection.
    oats_rcp = RecipeFactory('recipe_config/Oats.yml')
    # Get new class definitions from the collection.
    oats_class = oats_rcp('SteelCutOats')
    oats_class2 = oats_rcp('RolledOats')

    oats_inst = oats_class()
    oats_inst2 = oats_class2()

    print(f"Default SteelCutOats: Name: {rcp_inst.name()}, Cooking Time: {rcp_inst.cooking_time()}")
    print(f"Oats Collection SCO Name: {oats_inst.name()}, Cooking Time: {oats_inst.cooking_time()}")
    print(f"Oats Collection Rolled Name: {oats_inst2.name()}, Cooking Time: {oats_inst2.cooking_time()}")

    # A Composite Recipe
    oatmeal_fact = RecipeFactory('recipe_config/Oatmeal.yml')
    print(oatmeal_fact)