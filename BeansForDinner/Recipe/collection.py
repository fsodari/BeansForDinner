from .recipe import Recipe, merge_config
from . import recipe_factory
import logging

class Collection(Recipe):
    def __new__(cls:Recipe, config:dict={}):
        """Makes a selection from 'variants' based on config, then returns a Recipe object using RecipeFactory"""
        logging.info(f"Collection Config: {config}")
        # If no choice or the choice is not in the variants, use the default.
        if 'which' in config and config['which'] in config['variants']:
            which = config['which']
        else:
            which = next(iter(config['variants'])) # Invalid choice
        
        # Create a new recipe using the choice
        recipe_choice = config['variants'][which]
        # Apply the config overrides, but keep 'source' unchanged to keep the choice source.
        merge_config(recipe_choice, config, skip_source=True)
        # Override name using the which key
        recipe_choice['name'] = which

        logging.info(f"Collection Choice: {recipe_choice}")
        return recipe_factory.RecipeFactory(recipe_choice)
