# Recipe Factory

The recipe factory will take in a configuration dictionary as an argument, then return a class using the recipe information provided. The config dict can be a path to a recipe source file, or it could contain the full recipe definition. Based on the config information, the Recipe Factory will choose whether to return an Atomic Recipe, Collection Recipe, or Composite Recipe.

This will demonstrate the absolute minimum required to create each recipe type.

---

## Atomic Recipe Creation

If an empty or non-existent source file is used, the Recipe Factory will return an Atomic Recipe with the file name as the recipe name. You may also create an Atomic Recipe using at a minimum the name field.

Example SteelCutOats.yml file:

    name: Steel Cut Oats
    cooking_time: 14.0
    serving_size: 100.0

Usage:

    steel = RecipeFactory({'source':'SteelCutOats.yml'})

Once you've obtained the instance, you can override the default configuration.

    steel.override({'cooking_time':3.14})

Then the instance, with the base class methods, can be used with the html/md generator.

    assert steel.rcp['name'] == 'Steel Cut Oats'
    assert steel.rcp['cooking_time'] == 14.0

---

## Collection Recipe Creation

Collection Recipes must include a 'variants' field in their definition. Collections are a dict of recipes with custom overrides. They are a means of organizing recipes into useful categories. When instantiating a collection, a 'which' parameter can be specified. This should be the key for which recipe to select from 'variants'. Collections can supply a default 'which'. If not supplied, the first recipe in the dict will be used.

Oats.yml recipe file:

    name: Oats
    which: Steel Cut Oats
    variants:
      Steel Cut Oats:
        source: SteelCutOats.yml
        cooking_time: 14.3 # Collections can override defaults
      Rolled Oats:
        source: RolledOats.yml

Just like the other recipe types, recipe definitions can be substituted instead of source files.

You can supply any overrides after instantiation.

    oats = RecipeFactory({'which':'Rolled Oats', 'source':'Oats.yml'})
    oats.override({'cooking_time':42.0})

---

## Composite Recipe Creation
Composite Recipes must contain an 'ingredients' field in their definition. Ingredients is a dict of other recipes used in the main recipe. The key name is the ingredient label. It should be generic and descriptive. Ingredients may be any other recipe class.

Ingredient entries may use an 'amount' override to specify a serving size multiplier. 1.0 is used if no override is given.

Serving sizes may be extremely variable, so amount overrides will be common to make changing things easy. Users and recipe designers should be expected to adjust amounts when changing ingredients so this needs to be a UI knob that's easy to adjust and displays the final ingredient amount in real time.

The ingredient entries will be created like any other recipe. You may specify a source file or you may use a recipe definition.

Example Oatmeal.yml recipe file:

    name: Oatmeal
    ingredients:
      base:
        source: SteelCutOats.yml
        amount: 1.25 
      liquid:
        name: Water
        amount: 1.0
        serving_size: 100.0

Ingredients can be overriden in the recipe factory user config or as overrides after initialization.

    oatmeal = RecipeFactory({'source':'Oatmeal.yml'})
    oatmeal.override({'ingredients':{'base':{'source':'Quinoa.yml'}}})

You must provide a complete recipe definition when overriding ingredients. All existing ingredient information will replaced with the new configuration.

---
## Additional Notes

Tuples/Lists can be supported as a Composite. The recipe factory can use integers for keys and come up with sensible defaults for names, amounts, etc. This way you can swap 'lentils' for 'beans, cabbage, and rice' without too much hassle.
