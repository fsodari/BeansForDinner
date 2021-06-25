from BeansForDinner import Recipe
from BeansForDinner.Recipe import recipe_title

# Here are examples of user-defined recipes.
# Even simple ingredients need a class. But this can probably all be created with a factory or something from yaml files idk
class Salt(Recipe):
    def name(self):
        return "salt"

class SteelCutOats(Recipe):
    def name(self) -> str:
        return 'steel cut oats'

    def cooking_time(self) -> float:
        return 15.0

class RolledOats(Recipe):
    def name(self) -> str:
        return 'rolled oats'

    def cooking_time(self) -> float:
        return 5.0

class Water(Recipe):
    def name(self) -> str:
        return 'water'

    # def cooking_time(self) -> float:
    #     return 5 # cook water? boil water?

# Ingredients can be combined into a recipe with variations.
# Variations determine how the recipe is configured at initialization,
# but we can change things later still.

# A collection of recipes. You can do interesting things with this i think.
# For example, a recipe for "grains" with a lot of variety. Or a recipe for "cooked grains".
# which would also include recipes for common cooking methods/times. 
# Literally anything. Like spice blend variations, or preparation styles.
# This lets recipe designers(or modifiers) make generic recipes with sensible options.
# They are 'virtual' so there must be a default.
class Oats(Recipe):
    # 'Collections' need to define the __new__ method.
    def __new__(cls, which:Recipe=SteelCutOats):
        variants = [SteelCutOats, RolledOats]
        # Check if which is in variants?
        # Customize instance if you want
        return which()

# Composite recipes take ingredients as arguments.
class Oatmeal(Recipe):
    # Composite recipes have all ingredients passed as arguments
    def __init__(self, base:Recipe=Oats(), liquid:Recipe=Water(), seasoning:Recipe=Salt()):
        self.base = base
        self.liquid = liquid
        self.seasoning = seasoning

    def name(self) -> str:
        return 'oatmeal'
    
    def cooking_time(self) -> float:
        return self.base.cooking_time() + self.liquid.cooking_time() + self.seasoning.cooking_time()
    
    # Decorated title.
    def title(self):
        # Use the name for the title, but it could use something different.
        return f"{self.name()} using {self.base.name()}"

    def foo_title(self):
        # Use the name for the title, but it could use something different.
        return f"{self.name()} using {self.base.name()}"

    # Overridden formatting options.
    def _title_header(self) -> str:
        return "*O*A*T*S*O*A*T*S*O*A*T*S*O*A*T*S*\n\n"

if __name__ == '__main__':
    # Get an instance of a recipe with custom ingredients supplied
    breakfast = Oatmeal(base=Oats(SteelCutOats))

    # Decorate the title with a fancy header.
    formatted_title = recipe_title(Oatmeal.title)
    print(formatted_title(breakfast))
    print(breakfast.cooking_time())

