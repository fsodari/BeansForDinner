"""Composites contain a dictionary of ingredients.
Ingredients are other recipes and their overrides that are used in the composite recipe.
Composites share the same interface as atomics, and when calling methods like 'cooking_time()',
a composite will iterate through all its ingredients and compute the result.

A composite can be built from a dictionary of ingredients or from a list. If built from a list,
the keys will the integer indices converted to a decimal string.
"""

from .recipe import Recipe, ingr_iter
from . import recipe_factory
import logging

def list2dict(ilist) -> dict:
    """The indices of the list are converted to strings and used as keys for the new dict. If a dict is passed in,
    it will return it unchanged."""
    if isinstance(ilist, dict):
        return ilist
    else:
        return {str(i):ilist[i] for i in range(len(ilist))}

class Composite(Recipe):
    def __init__(self, config) -> None:
        """If the top level config is a list, then this will create a new composite using
        the list for the ingredients. """ 
        super().__init__()
        logging.info(f"Composite Init Config: {config}")

        try:
            # Test if config is a list-like object
            slice_test = config[:0]
            logging.info("Composite List")

            # Create ingredients from config.
            self.rcp['ingredients'] = list2dict(config)
            self._ingredients = {k:recipe_factory.RecipeFactory(ingr_cfg) for k, ingr_cfg in list2dict(config).items()}
            # Create a name derived from the ingredient names.
            self.rcp['name'] = ' and '.join([ingr.name() for k, ingr in self.ingredients().items()])
        except TypeError:
            # Using a config dict.
            self.rcp = Recipe.merge_config(self.rcp, config, merge_ingr=True)
            self._ingredients = {}
            # Convert to dict
            self.rcp['ingredients'] = list2dict(self.rcp['ingredients'])
            for k, ingr_cfg in self.rcp['ingredients'].items():
                logging.info(f"Ingr: {ingr_cfg}")
                self._ingredients[k] = recipe_factory.RecipeFactory(ingr_cfg)

        logging.info(f"Composite Final: {self.rcp}")
    
    def ingredients(self):
        return self._ingredients

    def override(self, config:dict) -> None:
        # Override default ingredients
        if 'ingredients' in config:
            for k, ingr_cfg in config['ingredients'].items():
                self.rcp['ingredients'][k] = ingr_cfg
                # Ingredients must be rebuilt if overridden.
                self._ingredients[k] = recipe_factory.RecipeFactory(ingr_cfg)

    def name(self) -> str:
        return self.rcp['name']

    def cooking_time(self) -> float:
        # Sum all ingredients cooking time.
        return sum([ingr.cooking_time() for k, ingr in self.ingredients().items()])