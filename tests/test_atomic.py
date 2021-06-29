from BeansForDinner import RecipeFactory
import pytest

import logging
# logging.basicConfig(filename='tests/logs/atomic.log', encoding='utf-8', level=logging.DEBUG)
atomic_logger = logging.getLogger('AtomicLogger')

def test_atomic_defaults():
    rcpf = RecipeFactory(logger=atomic_logger)

    steel_class = rcpf.get({'source':'test_recipes/SteelCutOats.yml'})
    steel_inst = steel_class()
    # This should follow default arguments
    assert steel_inst.rcp['name'] == 'Steel Cut Oats'
    assert steel_inst.rcp['cooking_time'] == 14.0

def test_atomic_overrides():
    rcpf = RecipeFactory(logger=atomic_logger)

    steel_class = rcpf.get({'source':'test_recipes/SteelCutOats.yml'})    

    # Supply config overrides at construction.
    steel_inst = steel_class({'name':'sco', 'cooking_time':3.14})
    assert steel_inst.rcp['name'] == 'sco'
    assert steel_inst.rcp['cooking_time'] == 3.14

def test_atomic_empty():
    rcpf = RecipeFactory(logger=atomic_logger)

    # Recipes must be named!
    with pytest.raises(KeyError):
        what_class = rcpf.get({})

    # Try reading a non-existant recipe from source.
    foo_class = rcpf.get({'source':'test_recipes/Foo.yml'})
    foo_inst = foo_class()
    assert foo_inst.rcp['name'] == 'Foo'

    # Try reading a recipe from an empty file
    water_class = rcpf.get({'source':'test_recipes/Water.yml'})
    water_inst = water_class()
    assert water_inst.rcp['name'] == 'Water'
