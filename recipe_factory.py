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
def CollectionFactory(config:dict, which:str):
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
# Need to get instances of all classes.
def composite_init(self:Recipe, defaults:dict, params:dict={}):
    # Override defaults
    for p in params:
        if p in defaults:
            defaults[p] = params[p]
    # Update the ingredients member to have instances of all classes.
    self.ingredients = {k:defaults[k]() for k in defaults}

# params is a dict of classes.
def CompositeRecipeFactory(config:dict):
    methods = get_main_methods(config, {})
    # Add default classes.
    defaults = {k:RecipeFactory(config['ingredients'][k]['source'])() for k in config['ingredients']}

    # Init method takes optional parameters
    methods['__init__'] = lambda self, params={}: composite_init(self, defaults, params)
    # methods['ingredients'] = lambda self: 
    return type(config['name'], (Recipe,), methods)


def RecipeFactory(config_file:str):
    # Read in yaml file.
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    # Collections implementation.
    if 'variants' in config:
        return lambda which: CollectionFactory(config, which)
    # Composite implementation
    elif 'ingredients' in config:
        return lambda: CompositeRecipeFactory(config)
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
    oatmeal_class = oatmeal_fact()
    # Default
    oatmeal_inst = oatmeal_class()
    print(f"Oatmeal: Name: {oatmeal_inst.name()}")
    print(f"Oatmeal Base: {oatmeal_inst.ingredients['base'].name()}, Liquid: {oatmeal_inst.ingredients['liquid'].name()}")

    # Use a different ingredient from the oats collection
    oatmeal_inst2 = oatmeal_class({'base':oats_rcp('RolledOats')})

    print(f"Oatmeal2 Base: {oatmeal_inst2.ingredients['base'].name()}, Liquid: {oatmeal_inst2.ingredients['liquid'].name()}")
    # This could be implemented in the base class
    total_cook_time = 0
    for i in oatmeal_inst.ingredients:
        total_cook_time += oatmeal_inst.ingredients[i].cooking_time()
    print(f"Total Cook Time: {total_cook_time}")

