import logging

# Base Class that all ingredients/recipes should inherit from.
class Recipe:
    # This is the attribute where recipe information is stored.
    def __init__(self) -> None:
        self.rcp = {}
        logging.info(f"Recipe Init")

    def override(self, config:dict) -> None:
        pass

    # Replace any top level keys in orig with those in new. Also add any keys in new that are not in orig.
    # Optionally apply the same merge to variants and ingredients lists.
    @staticmethod
    def merge_config(orig_:dict, new:dict, merge_var=False, merge_ingr=False) -> dict:
        orig = orig_
        for k in new:
            if k != 'variants' and k != 'ingredients':
                orig[k] = new[k]
        if 'variants' in new and merge_var:
            for k in new['variants']:
                orig['variants'][k] = new['variants'][k]
        if 'ingredients' in new and merge_ingr:
            for k in new['ingredients']:
                orig['ingredients'][k] = new['ingredients'][k]
        return orig

    # These are detailed formatting options. They can be overridden with user customizations if you're getting super custom.
    def _title_header(self) -> str:
        return "*******************************\n\n"
    
    def _title_footer(self) -> str:
        return "\n\n*******************************\n\n"
    
# Decorators provided with the Recipe base class to format and organize the process.
# Creates a formatted title.
def recipe_title(func):
    def wrapper(rcp:Recipe) -> str:
        # decorated function should return a string for the title name.
        # This example uses base class members, that can be overwritten by subclasses.
        return rcp._title_header() + func(rcp) + rcp._title_footer()
    return wrapper
