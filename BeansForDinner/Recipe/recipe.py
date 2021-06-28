from abc import ABC

# Base Class that all ingredients/recipes should inherit from.
class Recipe(ABC):
    # These are formatting options you may want to update, but this will se a sensible default
    def title(self) -> str:
        return self.name()

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
