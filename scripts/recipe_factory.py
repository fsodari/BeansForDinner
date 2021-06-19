import yaml
from recipe import Recipe
from recipe import SteelCutOats
from yaml import safe_load

# Create a class dynamically using:
# Class = type('ClassName', (Recipe,), {'__init__': __init__, 'printX': printX})

# The recipe factory will create new recipe classes from human-readable yaml files, recipe templates
# or from the user interface tools.

# Generic init function containing all required members.
# Use a higher order function to wrap this
def __rcp_init__(self:Recipe, name:str, cooking_time:float):
    # Always call base class init to make sure the 'backend' is set up.
    super(Recipe, self).__init__()
    self.name = name
    self.cooking_time = cooking_time

def __rcp_new__(cls:Recipe, which:Recipe):
    return super(cls, which).__new__()

class RecipeFactory:
    def __new__(cls, config_file:str=None):
        # Read in yaml file.
        with open(config_file, 'r') as stream:
            config = safe_load(stream)
        # Collections need a different implementation.
        if config['collection']:
            new_func = lambda cls, which: __rcp_new__(cls, which)
            new_rcp = type(config['name'], (Recipe,),{'__new__':new_func})
        else:
            # Wrap generic rcp_init with a higher level function using config arguments.
            init_func = lambda self: __rcp_init__(self, name=config['name'], cooking_time=config['cooking time'])
            # Create the new class.
            new_rcp = type(config['name'], (Recipe,),{'__init__': init_func})

        return new_rcp

if __name__ == '__main__':
    # Get a new recipe class from a yaml template. Neat.
    sco_rcp = RecipeFactory('scripts/steel_cut_oats.yml')
    # Get an instance of the class.
    rcp_inst = sco_rcp()

    oats_rcp = RecipeFactory('scripts/oats.yml')
    oats_inst = oats_rcp(SteelCutOats)

    print(f"Recipe Name: {rcp_inst.name}, Cooking Time: {rcp_inst.cooking_time}")
    print(f"Recipe Name: {oats_inst.name}, Cooking Time: {oats_inst.cooking_time}")
