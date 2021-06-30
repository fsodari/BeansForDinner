from BeansForDinner import RecipeFactory

import logging
# logging.basicConfig(filename='tests/logs/composite.log', encoding='utf-8', level=logging.DEBUG)
composite_logger = logging.getLogger('CompositeLogger')

def test_basic():
    oatmeal_inst = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    assert oatmeal_inst.rcp['name'] == 'Oatmeal'
    assert oatmeal_inst.rcp['ingredients']['base'].rcp['cooking_time'] == 11.1

    # You cannot reuse a class created from RecipeFactory. It must be a new instance.
    oats2 = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    oats2.override({'ingredients':{'base':{'source':'test_recipes/RolledOats.yml'}}})
    assert oats2.rcp['name'] == 'Oatmeal'
    assert oats2.rcp['ingredients']['base'].rcp['name'] == 'Rolled Oats'
