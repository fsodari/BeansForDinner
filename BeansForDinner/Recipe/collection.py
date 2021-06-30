from .recipe import Recipe
from . import recipe_factory
import logging

class Collection(Recipe):
    def __new__(cls:Recipe, config:dict={}):
        logging.info(f"Collection Config: {config}")
        # If no default given, the first element is used.
        if 'which' in config:
            # If the choice is not in the variants, use the default.
            if config['which'] in config['variants']:
                which = config['which']
            else:
                which = next(iter(config['variants'])) # Invalid choice
        else:
            which = next(iter(config['variants']))
        
        # Create a new recipe using the choice
        recipe_choice = config['variants'][which]
        logging.info(f"Collection Choice: {recipe_choice}")
        obj = recipe_factory.RecipeFactory(recipe_choice)
        # Apply the collection overrides.
        obj.override(recipe_choice)
        return obj