from BeansForDinner import RecipeFactory

import logging
# logging.basicConfig(filename='tests/logs/collection.log', encoding='utf-8', level=logging.DEBUG)
collection_logger = logging.getLogger('CollectionLogger')

def test_collection_default():

    oats_inst = RecipeFactory({'source':'test_recipes/Oats.yml'})
    print(oats_inst)
    assert oats_inst.rcp['name'] == 'rollllled oats'
    # Make sure it's using the class overrides
    assert oats_inst.rcp['cooking_time'] == 5.0

def test_collection_option():
    # Select a different option, must override which.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml', 'which':'Steel Cut Oats'})
    assert oats.rcp['name'] == 'Steel Cut Oats'
    assert oats.rcp['cooking_time'] == 13.0

def test_collection_new():
    # If the choice is not in the collection, default is created.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml', 'which':'Groats'})
    assert oats.rcp['name'] == 'Steel Cut Oats'

    # Overriding collection with variant override.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml','which':'Groats','variants':{'Groats':{'name':'Groats','cooking_time':20.0}}})
    assert oats.rcp['name'] == 'Groats'
    assert oats.rcp['cooking_time'] == 20.0

def test_collection_overrides():
    # Test overriding paramters of recipes in the collection.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml', 'which':'Steel Cut Oats'})
    # Overrides are just like any other recipe.
    oats.override({'name':'SCO','cooking_time':42.0})
    assert oats.rcp['name'] == 'SCO'
    assert oats.rcp['cooking_time'] == 42.0
