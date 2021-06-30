from BeansForDinner import RecipeFactory
import pytest

import logging
# logging.basicConfig(filename='tests/logs/atomic.log', encoding='utf-8', level=logging.DEBUG)
atomic_logger = logging.getLogger('AtomicLogger')

def test_atomic_defaults():
    steel_inst = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})

    # This should follow default arguments
    assert steel_inst.rcp['name'] == 'Steel Cut Oats'
    assert steel_inst.rcp['cooking_time'] == 14.0

def test_atomic_overrides():
    steel_inst = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})    
    # Overrides at construction.
    steel_inst.override({'name':'sco', 'cooking_time':3.14})

    assert steel_inst.rcp['name'] == 'sco'
    assert steel_inst.rcp['cooking_time'] == 3.14

def test_atomic_empty():
    # Recipes must be named!
    with pytest.raises(KeyError):
        what_class = RecipeFactory({})

    # Try reading a non-existant recipe from source.
    foo_inst = RecipeFactory({'source':'test_recipes/Foo.yml'})
    assert foo_inst.rcp['name'] == 'Foo'

    # Try reading a recipe from an empty file
    water_inst = RecipeFactory({'source':'test_recipes/Water.yml'})
    assert water_inst.rcp['name'] == 'Water'
