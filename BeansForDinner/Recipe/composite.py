from .recipe import Recipe
from . import recipe_factory
import logging

# Composites contain a dictionary of ingredients.
# Ingredients are other recipes and their overrides that are used in the composite recipe.
class Composite(Recipe):
    def __init__(self, config, from_list=False) -> None:
        super().__init__()
        logging.info(f"Composite Init Config: {config}")
        # Build a composite using the supplied list as the ingredients list.
        # Create a name by concatenating the items. "a, b, and c"
        if from_list:
            logging.info(f"Composite From List.")
            # Create a dumb name
            self.rcp['name'] = ' and '.join([ingr['name'] for ingr in config])
            # Create ingredients
            self.rcp['ingredients'] = {}
            for ingr_cfg in config:
                ingr_rcp = recipe_factory.RecipeFactory(ingr_cfg)
                ingr_rcp.override(ingr_cfg)
                self.rcp['ingredients'][ingr_cfg['name']] = ingr_rcp
        # Build a composite from the supplied definition.
        else:
            self.rcp = Recipe.merge_config(self.rcp, config, merge_ingr=True)
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
