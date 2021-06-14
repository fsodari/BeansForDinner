import logging, sys
logging.basicConfig(filename='logs/RecipeLog.log', level=logging.DEBUG)
from yaml import safe_load

# Base Class that all ingredients/recipes should inherit from.
class Recipe(object):
    def __init__(self, name):
        self.name = name
        logging.info(f'Recipe Name: {name}.')
