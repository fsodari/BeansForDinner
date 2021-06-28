from BeansForDinner.Recipe.recipe import Recipe
import pytest
from BeansForDinner import RecipeFactory

def test_atomic_defaults():
    steel_class = RecipeFactory({'source':'recipe_config/SteelCutOats.yml'})
    steel_inst = steel_class()
    print(steel_inst.rcp)
    # This should follow default arguments
    assert steel_inst.rcp['name'] == 'Steel Cut Oats'
    assert steel_inst.rcp['cooking_time'] == 14.0

def test_atomic_overrides():
    steel_class = RecipeFactory({'source':'recipe_config/SteelCutOats.yml'})    
    # Supply config overrides at construction.
    steel_inst = steel_class({'name':'sco', 'cooking_time':3.14})
    assert steel_inst.rcp['name'] == 'sco'
    assert steel_inst.rcp['cooking_time'] == 3.14

def test_atomic_empty():
    # Recipes must be named!
    with pytest.raises(KeyError):
        what_class = RecipeFactory({})
    
    # Try reading a non-existant recipe from source.
    foo_class = RecipeFactory({'source':'recipe_config/Foo.yml'})
    foo_inst = foo_class()
    assert foo_inst.rcp['name'] == 'Foo'

    # Try reading a recipe from an empty file
    water_class = RecipeFactory({'source':'recipe_config/Water.yml'})
    water_inst = water_class()
    assert water_inst.rcp['name'] == 'Water'

def test_composite_basic():
    oatmeal_class = RecipeFactory({'source':'recipe_config/Oatmeal.yml'})
    oatmeal_inst = oatmeal_class()
    assert oatmeal_inst.rcp['name'] == 'Oatmeal'
    print(oatmeal_inst.rcp['ingredients']['base'].rcp['name'])
    assert oatmeal_inst.rcp['ingredients']['base'].rcp['cooking_time'] == 11.1

    # You cannot reuse a class created from RecipeFactory. It must be a new instance.
    oatmeal2 = RecipeFactory({'source':'recipe_config/Oatmeal.yml'})
    oats2 = oatmeal2({'ingredients':{'base':{'source':'recipe_config/RolledOats.yml'}}})
    assert oats2.rcp['name'] == 'Oatmeal'
    assert oats2.rcp['ingredients']['base'].rcp['name'] == 'Rolled Oats'

def test_collection_default():
    oats_class = RecipeFactory({'source':'recipe_config/Oats.yml'})
    oats_inst = oats_class()
    assert oats_inst.rcp['name'] == 'rollllled oats'
    # Make sure it's using the class overrides
    assert oats_inst.rcp['cooking_time'] == 5.0

def test_collection_option():
    # Select a different option.
    oats_class = RecipeFactory({'source':'recipe_config/Oats.yml'})
    oats = oats_class({'which':'Rolled Oats'})
    assert oats.rcp['name'] == 'rollllled oats'
    assert oats.rcp['cooking_time'] == 5.0

def test_collection_new():
    # If the choice is not in the collection, default is created.
    oats_class = RecipeFactory({'source':'recipe_config/Oats.yml'})
    oats = oats_class({'which':'Groats'})
    assert oats.rcp['name'] == 'Steel Cut Oats'

    # Overriding collection with variant override.
    oats_class = RecipeFactory({'source':'recipe_config/Oats.yml'})
    oats = oats_class({'which':'Groats','variants':{'Groats':{'name':'Groats','cooking_time':20.0}}})
    assert oats.rcp['name'] == 'Groats'
    assert oats.rcp['cooking_time'] == 20.0

def test_collection_overrides():
    # Test overriding paramters of recipes in the collection.
    oats_class = RecipeFactory({'source':'recipe_config/Oats.yml'})
    oats = oats_class({'which':'Steel Cut Oats','variants':{'Steel Cut Oats':{'name':'SCO'}}})
    assert oats.rcp['name'] == 'SCO'
    assert oats.rcp['cooking_time'] == 13.0
