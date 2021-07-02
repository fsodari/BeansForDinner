import logging
import yaml

def ingr_iter(thething):
    if isinstance(thething, dict):
        return thething
    else:
        return range(len(thething))

def list2dict(ilist) -> dict:
    """The indices of the list are converted to strings and used as keys for the new dict. If a dict is passed in,
    it will return it unchanged."""
    if isinstance(ilist, dict):
        return ilist
    else:
        return {str(i):ilist[i] for i in range(len(ilist))}

def merge_config(orig:dict, new:dict, r_fields:list=[], banned:list=[]) -> dict:
    """ Merge two configuration dictionaries. Variants and Ingredients get merged independently.
        Entries in orig and new are overwritten by new.
        Entries in new but not orig are appended to orig.
        Entries in orig but not new are unchanged.
        r_fields is a list of fields to be merged recursively.
        banned is a list of fields to not copy
    """
    merged = orig
        
    banned.extend(['variants','ingredients'])
    # Update top level fields.
    for k in new:
        if k not in banned:
            merged[k] = new[k]

    # r_fields are fields that will be recursively merged like 'variants' or 'ingredients'
    for f in r_fields:
        if f in new:
            # Create new dict key
            if f not in merged:
                merged[f] = list2dict(new[f])
            # Update entries if field exists already.
            else:
                for k, v in list2dict(new[f]).items():
                    merged[f][k] = v
            
    return merged

# Base Class that all ingredients/recipes should inherit from.
class Recipe:
    def __init__(self) -> None:
        """ Initialize recipe defaults """
        self.rcp = {}
        # Sensible defaults.
        self.rcp['name'] = 'noname'
        self.rcp['cooking time'] = 0.0
        self.rcp['units'] = 'g'
        self.rcp['density'] = 1.0 # kg/m**3. Need to give user a tool and procedure to add this. It's very optional though
        self.rcp['amount'] = 1.0 # using 'units'

        logging.info(f"Recipe Init")

    def override(self, config:dict) -> None:
        """ Override recipe configurations after the recipe has been initialized """
        # Merge everything by default.
        self.rcp = merge_config(self.rcp, config, r_fields=['variants', 'ingredients'])

    def name(self) -> str:
        """ Returns the recipes name as a str """
        return self.rcp['name']

    def cooking_time(self) -> float:
        """ Returns the recipe's cooking time as a float """
        return self.rcp['cooking time']

    def amount(self) -> float:
        return self.rcp['amount']

    def export(self, output_file:str):
        """
        Export recipe config as a yaml file.
        If 'source' exists as a top level parameter, it will be changed to 'original source'
        """
        with open(output_file, 'w') as stream:
            exp_cfg = self.rcp
            exp_cfg['original source'] = exp_cfg.pop('source')
            yaml.dump(self.rcp, stream, sort_keys=False)

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
