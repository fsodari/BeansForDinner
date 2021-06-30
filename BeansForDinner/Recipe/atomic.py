from .recipe import Recipe
import logging

# Atomic recipe factory. Atomic recipes have no ingredients.
class Atomic(Recipe):
    def __init__(self, config:dict={}) -> None:
        super().__init__()
        logging.info(f"Atomic Init Config: {config}")
        # Merge config
        self.rcp = config

    def override(self, config:dict={}):
        # self.rcp = self.rcp | config
        self.rcp = Recipe.merge_config(self.rcp, config)
        logging.info(f"Atomic Override: {self.rcp}")
