# Recipe Factory

The recipe factory will take in a configuration dictionary as an argument, then return a class using the recipe information provided. The config dict can be a path to a recipe source file, or it could contain the full recipe definition. Based on the config information, the Recipe Factory will choose whether to return an Atomic Recipe, Composite Recipe, or Collection Recipe.

This will demonstrate the absolute minimum required to create each recipe type.

---

## Atomic Recipe Creation

If an empty or non-existent source file is used, the Recipe Factory will return an Atomic Recipe with the file name as the recipe name. You may also create an Atomic Recipe using at a minimum the name field.

Example SteelCutOats.yml file:

    name: Steel Cut Oats
    cooking_time: 14.0
    serving_size: 100.0

Usage:

    sco_atomic = RecipeFactory({'source':'SteelCutOats.yml'})

Recipe factory using a non-existant file, and using a recipe definition instead of a file.

    foo_atomic = RecipeFactory({'source':'Foo.yml'})
    bar_atomic = RecipeFactory({'name':'Bar'})

Once you've obtained the class definition, you can create an instance of the class. During object initialization, you may override or extend the default configuration.

    sco_inst = sco_atomic() # default
    foo_inst = foo_atomic() # default
    bar_inst = bar_atomic({'cooking_time':42.0}) # override

Then the instance, with the base class methods, can be used with the html/md generator.

    assert sco_inst.rcp.name == 'Steel Cut Oats'
    assert sco_inst.rcp.cooking_time == 14.0

    assert foo_inst.rcp.name == 'Foo' # derived from filename
    assert foo_inst.rcp.cooking_time == 0.0 # Base class default
    assert bar_inst.rcp.name == 'Bar'
    assert bar_inst.rcp.cooking_time == 42.0 # Override

---

## Composite Recipe Creation
Composite Recipes must contain an 'ingredients' field in their definition. Ingredients is a dict of other recipes used in the main recipe. The key name is the ingredient label. It should be generic and descriptive. Ingredients may be individual recipes or they may be tuples.

Ingredient entries may use an 'amount' override to specify a serving size multiplier. 1.0 is used if no override is given.

Tuples will use 1/len(entry) for the default amount if none is specified. The amounts for tuples do not necessarily need to sum to 1.

Serving sizes may be extremely variable, so amount overrides will be common to make changing things easy. Users and recipe designers should be expected to set the ratio when changing ingredients so this needs to be a UI knob that's easy to adjust and updates the final ingredient amount in real time.

The ingredient entries will be created like any other recipe. You may specify a source file or you may use a recipe definition.

Example Oatmeal.yml recipe file:

    name: Oatmeal
    ingredients:
      Base:
        source: SteelCutOats.yml
        amount: 1.25 
      Liquid:
        # Tuple
        - name: Water
          amount: 1.0
          serving_size: 100.0 # By overriding serving_size as well, the final amount can be specified easily.
        - source: SoyMilk.yml
          amount: 0.1 # relative to SoyMilk's serving_size

Using the Recipe Factory:

    oatmeal_composite = RecipeFactory({'source':'Oatmeal.yml'})

Like atomics, any field can be overriden at object instantiation. This is where you can substitute new ingredients. Amounts should be overriden here as well, including the base entry amounts.

    quinoa_oatmeal = oatmeal_composite(
        {{'ingredients':{'Base':(
            {'source':'SteelCutOats.yml',   'amount': 1.0},
            {'source':'Quinoa.yml',         'amount': 0.2})}})

Top level parameters can be overriden as well just like with atomics. Additional ingredient recipes can also be appended at object creation too.

---

## Collection Recipe Creation

Collection Recipes must include a 'variants' field in their definition. Collections are a dict of recipes with custom overrides. They are a means of organizing recipes into useful categories. When instantiating a collection, a 'which' parameter can be specified. This should be the key for which recipe to select from 'variants'. Collections can supply a default 'which'. If not supplied, the first recipe in the dict will be used.

Oats.yml recipe file:

    name: Oats
    which: Steel Cut Oats # default choice.
    variants:
      Steel Cut Oats:
        source: SteelCutOats.yml
        cooking_time: 14.3 # Collections can override defaults
      Rolled Oats:
        source: RolledOats.yml

Just like the other recipe types, recipe definitions can be substituted instead of source files. Anything can be overriden including adding new variants. Variants can also be tuples just like ingredients in Composites.

To override something, you must override the entry in variants and also override 'which'. It's a bit verbose but the UI can handle that ;)

    oats_collection = RecipeFactory({'source':'Oats.yml'})
    oats_inst = oats_collection({'which':'Rolled Oats','variants':{'Rolled Oats':}})

---
## Additional Notes

With the way it works now, I think class definitions can't be reused. The overrides change the base class definition, so recipes will override each other. So each recipe instance must start with calling RecipeFactory. The user interface will just be compiling a config dict to pass to RecipeFactory, so this works out fine.