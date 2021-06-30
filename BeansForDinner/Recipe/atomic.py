from .recipe import Recipe
import logging

# Atomic recipe factory. Atomic accept no other recipes as inputs. They contain only the recipe configuration.
class Atomic(Recipe):
    def __init__(self, config:dict={}) -> None:
        super().__init__()
        logging.info(f"Atomic Init Config: {config}")
        # Config is whatever is passed into it.
        self.rcp = config

    def override(self, config:dict) -> None:
        # self.rcp = self.rcp | config
        self.rcp = Recipe.merge_config(self.rcp, config)
        logging.info(f"Atomic Override: {self.rcp}")
