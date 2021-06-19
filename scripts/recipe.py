import logging, sys
logging.basicConfig(filename='logs/RecipeLog.log', level=logging.DEBUG)
from yaml import safe_load




# Base Class that all ingredients/recipes should inherit from.
class Recipe:
    def __init__(self):
        # default formatting options. Can be something fancy like markup and templates.
        self._title_header = "*******************************\n\n"
        self._title_footer = "\n\n*******************************\n\n"

        # These are required members that every recipe needs to set.
        self.name = 'name'
        self.variants = [] # Recipe specific customizations.
        self.which_var = '' # Which variation is selected for this instance.
        self.cooking_time = 0

# Decorators provided with the Recipe base class to format and organize the process.
# Creates a formatted title.
def recipe_title(func):
    def wrapper(rcp:Recipe):
        # decorated function should return a string for the title name.
        # This example uses base class members, that can be overwritten by subclasses.
        return rcp._title_header + func(rcp) + rcp._title_footer
    return wrapper

# sub-recipe? part? idk..
# This is a modular part of a recipe. These should be parts of the recipe like 
# 'filling', 'topping' 

# Here are examples of user-defined recipes.
# Even simple ingredients need a class. But this can probably all be created with a factory or something from yaml files idk
class Salt(Recipe):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        super().__init__()
        self.name = 'salt'

class SteelCutOats(Recipe):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        super().__init__()
        self.name = 'steel cut oats'
        self.cooking_time = 15

class RolledOats(Recipe):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        super().__init__()
        self.name = 'rolled oats'
        self.cooking_time = 5

class Water(Recipe):
    def __new__(cls):
        return super().__new__(cls)
    
    def __init__(self):
        super().__init__()
        self.name = 'water'

# Ingredients can be combined into a recipe with variations.
# Variations determine how the recipe is configured at initialization,
# but we can change things later still.

# A group of similar items. You can do interesting things with this i think.
# For example, a recipe for "grains" with a lot of variety. Or a recipe for "cooked grains".
# which would also include recipes for common cooking methods/times. 
# Literally anything. Like spice blend variations, or preparation styles.
# This lets recipe designers(or modifiers) make generic recipes with sensible options.
# They are 'virtual' so there must be a default.
class Oats(Recipe):
    def __new__(cls, which_var='steel cut'):
        variants = {'steel cut':SteelCutOats, 'rolled':RolledOats}
        return variants[which_var]()
    
    def __init__(self, which_var='steel cut'):
        super().__init__()

# Something that finally looks like a real recipe.
class Oatmeal(Recipe):
    def __new__(cls, which_var='steel cut'):
        return super().__new__(cls)

    def __init__(self, which_var='steel cut'):
        super().__init__()
        # Use a different header if you want to change from the default. Usually don't need to mess with these.
        self._title_header = "*O*A*T*S*O*A*T*S*O*A*T*S*O*A*T*S*\n\n"

        # Initialize the required parts of a recipe.
        self.name = "Oatmeal"
        self.variants = ['steel cut', 'rolled']
        # Need a yamlable way of doing this
        self.base = Oats(which_var)
        self.liquid = Water()
        self.seasoning = Salt()

        # These are the ingredients seperated into categories.
        # self.ingredients = {'base':Oats(which_var), 'liquid':Water(), 'seasoning':Salt()}
        # These are configuration dicts that can be imported from yaml files so it should be
        # very easy to generate these things automatically.

    # Use this method for the recipe title.
    @recipe_title
    def title(self):
        # Use the name for the title, but it could use something different.
        return f"{self.name} using {self.base.name}"

if __name__ == '__main__':
    breakfast = Oatmeal('steel cut')
    print(breakfast.title())

