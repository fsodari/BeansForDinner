from .recipe import Recipe
from . import recipe_factory
import logging

# Composites contain a dictionary of ingredients.
# Ingredients are other recipes and their overrides that are used in the composite recipe.
class Composite(Recipe):
    def __init__(self, config:dict={}) -> None:
        super().__init__()
        logging.info(f"Composite Init Config: {config}")
        self.rcp = config
        # Create ingredients.
        for k in self.rcp['ingredients']:
            logging.info(f"Ingr: {self.rcp['ingredients'][k]}")
            ingr_rcp = recipe_factory.RecipeFactory(self.rcp['ingredients'][k])
            ingr_rcp.override(self.rcp['ingredients'][k])
            # Override the config with a recipe class. What are types even really?
            self.rcp['ingredients'][k] = ingr_rcp

        logging.info(f"Composite Final: {self.rcp}")
    
    def override(self, config:dict) -> None:
        # Override default ingredients
        if 'ingredients' in config:
            for k in config['ingredients']:
                # Ingredients must be rebuilt if overridden.
                self.rcp['ingredients'][k] = recipe_factory.RecipeFactory(config['ingredients'][k])
