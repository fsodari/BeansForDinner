from .recipe import Recipe
from . import recipe_factory
import logging

class Collection(Recipe):
    def __new__(cls:Recipe, config:dict={}):
        logging.info(f"Collection Config: {config}")
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
        # Apply the config overrides, but keep 'source' unchanged.
        Recipe.merge_config(recipe_choice, config, skip_source=True)
        # Override name using the which key
        recipe_choice['name'] = which

        logging.info(f"Collection Choice: {recipe_choice}")
        return recipe_factory.RecipeFactory(recipe_choice)
