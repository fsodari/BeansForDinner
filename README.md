# Beans For Dinner Theory

Everything is a Recipe. This app will provide a Recipe base class that every class will inherit from. Everything from simple recipes like 'water' or 'steel cut oats', to more complex recipes like 'curry powder' or 'black bean enchiladas with red chili sauce' that are composites of other recipes. Since everything inherits from the same base class, everything can be modified, mixed, and matched.

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
Composite Recipes take other recipes as arguments. This would be something like "oatmeal" which takes "oats" and "liquid" as arguments. All recipes used in a composite recipe must be passed as inputs


Recipes will need to override certain base class methods/members like the name, cooking time, ingredients(other recipes), and cooking instructions. The base recipe class will use decorators(wrappers around functions) to add formatting to the user-supplied methods. Then the app will use the base class to do useful things like compile an ingredients list, generate a pretty markdown or html recipe, and save the recipe to a library.
  


    # Recipe base class.
    class Recipe(ABC):
        # Derived recipes must provide the required methods.
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
            # Use func should return a string with the title
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

        def cooking_time(self) -> float:
            return self.base.cooking_time() + self.liquid.cooking_time()
         
        def title(self):
            return f"{self.name} using {self.base.name} and {self.liquid.name}"

    # An instance of a recipe
    breakfast = Oatmeal(base=Oats(SteelCutOats))
    formatted_title = html_title(Oatmeal.title)
    print(formatted_title(breakfast))

Recipes that are composites can choose to override the

Lower level recipes

## Set up a python virtualenvironment

    python3 -m venv beans

## Install all requirements

    pip install -r requirements.txt

# Run the app using python

    python -m BeansForDinner

# Restart and Rebuild

    docker-compose build && docker-compose up -d
