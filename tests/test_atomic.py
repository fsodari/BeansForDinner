from BeansForDinner.Recipe import RecipeFactory
import pytest

def test_defaults():
    steel = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})

    # This should follow default arguments
    assert steel.name() == 'Steel Cut Oats'
    assert steel.cooking_time() == 14.0

def test_overrides():
    steel = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})    

    # Apply any overrides.
    steel.override({'name':'sco', 'cooking_time':3.14})

    assert steel.name() == 'sco'
    assert steel.cooking_time() == 3.14

def test_empty():
    # Recipes must be named!
    with pytest.raises(KeyError):
        what_class = RecipeFactory({})

    # Try reading a non-existant recipe from source.
    foo = RecipeFactory({'source':'test_recipes/Foo.yml'})
    assert foo.name() == 'Foo'

    # Try reading a recipe from an empty file
    water = RecipeFactory({'source':'test_recipes/Water.yml'})
    assert water.name() == 'Water'
