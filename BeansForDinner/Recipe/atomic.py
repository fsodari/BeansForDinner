from .recipe import Recipe, merge_config
import logging

# Atomic recipe factory. Atomic accept no other recipes as inputs. They contain only the recipe configuration.
class Atomic(Recipe):
    def __init__(self, config:dict={}) -> None:
        """Initialize atomic with recipe configuration."""
        super().__init__()
        logging.info(f"Atomic Init Config: {config}")
        self.rcp = merge_config(self.rcp, config)
        logging.info(f"Atomic Init: {self.rcp}")

    def override(self, config:dict) -> None:
        """Override recipe parameters"""
        logging.info(f"Atomic Override Config: {config}")
        self.rcp = merge_config(self.rcp, config)
        logging.info(f"Atomic Override: {self.rcp}")

    def ingredients(self) -> dict:
        """Atomics return themselves as their ingredients list."""
        return {'0':self}
