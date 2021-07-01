from .recipe import Recipe
from . import recipe_factory
from functools import reduce
import logging



# Composites contain a dictionary of ingredients.
# Ingredients are other recipes and their overrides that are used in the composite recipe.
class Composite(Recipe):
    def __init__(self, config) -> None:
        super().__init__()
        logging.info(f"Composite Init Config: {config}")
        try:
            # Test if config is a list-like object
            slice_test = config[:0]
            logging.info("Composite List")
            def build_recipe(cfg):
                the_recipe = recipe_factory.RecipeFactory(cfg)
                # Need to apply overrides if the recipe might be a collection.
                the_recipe.override(cfg)
                return the_recipe
            # Create ingredients
            self.rcp['ingredients'] = [build_recipe(ingr_cfg) for ingr_cfg in config]
            # Create a name derived from the ingredient names.
            self.rcp['name'] = ' and '.join([self.rcp['ingredients'][i].name() for i in self.ingr_iter()])
        except TypeError:
            # Using a config dict.
            self.rcp = Recipe.merge_config(self.rcp, config, merge_ingr=True)
            for i in self.ingr_iter():
                logging.info(f"Ingr: {self.rcp['ingredients'][i]}")
                ingr_rcp = recipe_factory.RecipeFactory(self.rcp['ingredients'][i])
                # Override in case the recipe was a collection.
                ingr_rcp.override(self.rcp['ingredients'][i])
                # Override the config with a recipe class. What are types even really?
                self.rcp['ingredients'][i] = ingr_rcp

        logging.info(f"Composite Final: {self.rcp}")
    
    def ingr_iter(self):
        """Returns an iterator based on the type of the ingredients list"""
        if isinstance(self.rcp['ingredients'], dict):
            return self.rcp['ingredients']
        else:
            return range(len(self.rcp['ingredients']))
        
    def ingredients(self):
        return self.rcp['ingredients']

    def override(self, config:dict) -> None:
        # Override default ingredients
        if 'ingredients' in config:
            for k in config['ingredients']:
                # Ingredients must be rebuilt if overridden.
                self.rcp['ingredients'][k] = recipe_factory.RecipeFactory(config['ingredients'][k])

    def name(self) -> str:
        return self.rcp['name']

    def cooking_time(self) -> float:
        # Sum all ingredients cooking time.
        return reduce(lambda a, b: a + b, [self.rcp['ingredients'][k].rcp['cooking_time'] for k in self.rcp['ingredients'].keys()])