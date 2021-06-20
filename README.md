# Beans For Dinner Theory

Everything is a Recipe. This app will provide a Recipe base class that every class will inherit from. Everything from simple recipes like 'water' or 'steel cut oats', to more complex recipes like 'curry powder' or 'black bean enchiladas with red chili sauce' that are composites of other recipes. Since everything inherits from the same base class, everything can be modified, mixed, and matched. This lets the user easily customize recipes with new ingredients and automatically generate formatted, shareable, printable, recipes.

## Primary Recipe Structures.

- Recipe Base Class

- Atomic Recipes

- Collections

- Composite Recipes

### Recipe Base Class

The Recipe Base Class will implement methods and decorators to format and organize the recipe. It will provide virtual methods that need to be overriden like the recipe name, cooking time, and cooking instructions. Everything will inherit from this class so that everything can easily be changed to a different recipe. The decorators provided will allow the subclass to return data in a simple format, then the base class decorator can format things for html, markdown, etc.

### Atomic Recipes

Atomic Recipes are subclasses of Recipe that take no other recipes as inputs. These would be simple recipes like "water" or "steel cut oats". So in order to build more complex recipes, Recipes for every ingredient must exist in the library. Atomic recipes may still have optional methods like cooking times and cooking instructions. Again, everything is a recipe. Everything can be extended or changed.

### Collections

Collections are implemented using a class factory. The collection would return a recipe instance based on some user input/choice. A simple example is "oats" as a collection of "steel cut oats" and "rolled oats". Collections exist to organize recipes into logical categories. These collections can also instantiate recipes in particular ways. For example, a collection of "mushy oats" could extend "oats", but increase the standard cooking time by 30%. When creating Composite Recipes, you can specify collections as the ingredient inputs as a sort of 'type hint' so that users customizing the recipe have a list of sane options to choose from. Collections can be anything. 'curry spice blends', 'grains', 'frank's top 10 enchilada fillings'. And these can be saved in the library just like any other recipe. I see these being very useful and powerful tools.

### Composite Recipes
Composite Recipes take other recipes as arguments. This would be something like "oatmeal" which takes "base" and "liquid" as arguments. All ingredients used in a composite recipe must be passed as inputs to the constructor, and they must be Recipe subclasses. Reasonable defaults using collections can be supplied, but anything can be passed to a recipe for customization.

Composite recipes are likely to supply more complex instructions that Atomic Recipes. They may want to use an ingredients suggested cooking time, or override it if needed. Recipe instructions should depend upon the ingredients methods as much as possible to make sure recipes can be exchanged. Composites could be content aware and change procedures based on the ingredients too.
  
## Examples

    # Recipe base class.
    class Recipe(ABC): # Abstract Base Class
        # Derived recipes must provide these required methods.
        @abstractmethod
        def name(self) -> str:
            pass
        # Optional methods
        def cooking_time(self) -> float:
            return 0.0
        # Optional and uses a reasonable default.
        def title(self) -> str:
            return self.name()

    # Decorators for recipe formatting/organization
    def html_title(func):
        def wrapper(rcp:Recipe) -> str:
            # Subclass title method should return a string with the title
            recipe_title = func(rcp)
            return pretty_html_title(recipe_title)
        return wrapper

    # Derived recipes.
    # Simple ingredients take no arguments.
    class SteelCutOats(Recipe):
        def name(self) -> str:
            return 'steel cut oats'
        def cooking_time(self) -> float:
            return 15.0

    # Collections are factories that create and initialize a recipe instance based on user parameters. They are 'virtual' and return other classes. Collections can initialize recipes in specific ways as well.
    class Oats(Recipe):
        def __new__(cls, which:Recipe=SteelCutOats):
            variants = [SteelCutOats, RolledOats]
            return which()

    # Composite recipes take recipes as parameters so that different recipes can be swapped in and out.
    class Oatmeal(self, base:Recipe=Oats(), liquid:Recipe=Water()):
        def __init__(self):
            self.base = base
            self.liquid = liquid
            self.cooking_time = self.base.cooking_time + self.liquid.cooking_time

        def name(self) -> str:
            return 'oatmeal'

        # Cooking time is based on ingredients used.
        def cooking_time(self) -> float:
            return self.base.cooking_time() + self.liquid.cooking_time()
        
        # Updated title
        def title(self):
            return f"{self.name} using {self.base.name} and {self.liquid.name}"

    # An instance of a recipe
    breakfast = Oatmeal(base=Oats(SteelCutOats))
    formatted_title = html_title(Oatmeal.title)
    print(formatted_title(breakfast))

    > (*fancy formatting*) oatmeal using steel cut oats and water


This demonstrates a proof of concept of this organizational pattern. If the recipes follow rules and templates, it seems like this should work. Extracting and compiling ingredients/instructions might be challenging, but it's a "solve it once" problem I hope.

## YAML Defined Classes
What? You don't think normal people will want to write recipes in python. No problem! It's python and it can do anything.

These recipe classes will mainly consist of methods returning strings and numbers. We can define recipes using human-readable yaml files, then use a RecipeFactory to create classes dynamically based on the configuration. As long as recipes stick to certain templates, the factory should be able to handle all method creation. These yaml templates can eventually be generated through a separate GUI app and any 'programmer files' would be abstracted away entirely.

recipe_factory.py shows an implementation using sample recipes stored in recipe_config


## Set up a python virtualenvironment

    python3 -m venv beans

## Install all requirements

    pip install -r requirements.txt

## Run the recipe_factory.py test

    python recipe_factory.py

    (run output)
    Default SteelCutOats: Name: Steel Cut Oats, Cooking Time: 14.0
    Oats Collection SCO Name: Steel Cut Oats, Cooking Time: 13.0
    Oats Collection Rolled Name: rollllled oats, Cooking Time: 5.0
    Oatmeal: Name: Oatmeal
    Oatmeal Base: Steel Cut Oats, Liquid: Water
    Oatmeal2 Base: Rolled Oats, Liquid: Water
    Total Cook Time: 14.1

## Run the recipe.py example
    python Recipe/recipe.py

    *O*A*T*S*O*A*T*S*O*A*T*S*O*A*T*S*

    oatmeal using steel cut oats

    *******************************


    15.0
