from BeansForDinner import RecipeFactory
import pytest

def test_atomic_defaults():
    steel_class = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})
    steel_inst = steel_class()
    # This should follow default arguments
    assert steel_inst.rcp['name'] == 'Steel Cut Oats'
    assert steel_inst.rcp['cooking_time'] == 14.0

def test_atomic_overrides():
    steel_class = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})    
    # Supply config overrides at construction.
    steel_inst = steel_class({'name':'sco', 'cooking_time':3.14})
    assert steel_inst.rcp['name'] == 'sco'
    assert steel_inst.rcp['cooking_time'] == 3.14

def test_atomic_empty():
    # Recipes must be named!
    with pytest.raises(KeyError):
        what_class = RecipeFactory({})
    
    # Try reading a non-existant recipe from source.
    foo_class = RecipeFactory({'source':'test_recipes/Foo.yml'})
    foo_inst = foo_class()
    assert foo_inst.rcp['name'] == 'Foo'

    # Try reading a recipe from an empty file
    water_class = RecipeFactory({'source':'test_recipes/Water.yml'})
    water_inst = water_class()
    assert water_inst.rcp['name'] == 'Water'
