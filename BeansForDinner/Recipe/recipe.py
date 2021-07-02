import logging
from os import stat

def ingr_iter(thething):
    if isinstance(thething, dict):
        return thething
    else:
        return range(len(thething))

# Base Class that all ingredients/recipes should inherit from.
class Recipe:
    def __init__(self) -> None:
        """ Initialize recipe defaults """
        self.rcp = {}
        # Sensible defaults.
        self.rcp['name'] = 'noname'
        self.rcp['cooking_time'] = 0.0
        self.rcp['units'] = 'g'
        self.rcp['density'] = 1.0 # kg/m**3. Need to give user a tool and procedure to add this. It's very optional though
        self.rcp['amount'] = 1.0 # using 'units'

        logging.info(f"Recipe Init")

    def override(self, config:dict) -> None:
        """ Override recipe configurations after the recipe has been initialized """
        # Merge everything by default.
        self.rcp = self.merge_config(self.rcp, config, merge_var=True, merge_ingr=True)

    def name(self) -> str:
        """ Returns the recipes name as a str """
        return self.rcp['name']

    def cooking_time(self) -> float:
        """ Returns the recipe's cooking time as a float """
        return self.rcp['cooking_time']

    def amount(self) -> float:
        return self.rcp['amount']

    @staticmethod
    def merge_config(orig_:dict, new:dict, merge_var=False, merge_ingr=False, skip_source=False) -> dict:
        """ Merge two configuration dictionaries. Variants and Ingredients get merged independently.
            Entries in orig and new are overwritten by new.
            Entries in new but not orig are appended to orig.
            Entries in orig but not new are unchanged. """
        orig = orig_
        for k in new:
            if k != 'variants' and k != 'ingredients':
                if k != 'source' or not skip_source:
                    orig[k] = new[k]
        if 'variants' in new and merge_var:
            if 'variants' not in orig:
                orig['variants'] = new['variants']
            else:
                for k in new['variants']:
                    orig['variants'][k] = new['variants'][k]
        if 'ingredients' in new and merge_ingr:
            if 'ingredients' not in orig:
                orig['ingredients'] = new['ingredients']
            else:
                for k in new['ingredients']:
                    orig['ingredients'][k] = new['ingredients'][k]
        return orig

    # These are detailed formatting options. They can be overridden with user customizations if you're getting super custom.
    def _title_header(self) -> str:
        """Returns a formatted recipe title header as a str"""
        return "*******************************\n\n"
    
    def _title_footer(self) -> str:
        """Returns a formatted recipe title footer as a str"""
        return "\n\n*******************************\n\n"
    
# Decorators provided with the Recipe base class to format and organize the process.
# Creates a formatted title.
def recipe_title(func):
    """Wraps the recipe title with a header and footer and returns a str"""
    def wrapper(rcp:Recipe) -> str:
        # decorated function should return a string for the title name.
        # This example uses base class members, that can be overwritten by subclasses.
        return rcp._title_header() + func(rcp) + rcp._title_footer()
    return wrapper
