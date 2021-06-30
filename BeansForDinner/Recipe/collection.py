from .recipe import Recipe
import logging
try: from .recipe_factory import RecipeFactory
except ImportError: pass

class Collection(Recipe):
    def __new__(cls:Recipe, config:dict={}) -> Recipe:
        logging.info(f"Collection Overrides: {config}")
        
        # If no default given, the first element is used.
        if 'which' in config:
            if config['which'] in config['variants']:
                which = config['which']
            else:
                which = next(iter(config['variants'])) # Invalid choice
        else:
            which = next(iter(config['variants']))
        
        # Create a new recipe using the choice
        recipe_choice = config['variants'][which]
        logging.info(f"Collection Choice: {recipe_choice}")
        obj = RecipeFactory(recipe_choice)
        obj.override(recipe_choice)
        return obj
