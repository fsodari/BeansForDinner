from BeansForDinner import RecipeFactory

import logging
# logging.basicConfig(filename='tests/logs/collection.log', encoding='utf-8', level=logging.DEBUG)
collection_logger = logging.getLogger('CollectionLogger')

def test_collection_default():
    rcpf = RecipeFactory(logger=collection_logger)

    oats_class = rcpf.get({'source':'test_recipes/Oats.yml'})
    oats_inst = oats_class()
    assert oats_inst[0].rcp['name'] == 'rollllled oats'
    # Make sure it's using the class overrides
    assert oats_inst[0].rcp['cooking_time'] == 5.0

def test_collection_option():
    rcpf = RecipeFactory(logger=collection_logger)

    # Select a different option.
    oats_class = rcpf.get({'source':'test_recipes/Oats.yml'})
    oats = oats_class({'which':'Steel Cut Oats'})
    assert oats[0].rcp['name'] == 'Steel Cut Oats'
    assert oats[0].rcp['cooking_time'] == 13.0

def test_collection_new():
    rcpf = RecipeFactory(logger=collection_logger)

    # If the choice is not in the collection, default is created.
    oats_class = rcpf.get({'source':'test_recipes/Oats.yml'})
    oats = oats_class({'which':'Groats'})
    assert oats[0].rcp['name'] == 'Steel Cut Oats'

    # Overriding collection with variant override.
    oats_class = rcpf.get({'source':'test_recipes/Oats.yml'})
    oats = oats_class({'which':'Groats','variants':{'Groats':[{'name':'Groats','cooking_time':20.0}]}})
    assert oats[0].rcp['name'] == 'Groats'
    assert oats[0].rcp['cooking_time'] == 20.0

def test_collection_overrides():
    rcpf = RecipeFactory(logger=collection_logger)

    # Test overriding paramters of recipes in the collection.
    oats_class = rcpf.get({'source':'test_recipes/Oats.yml'})
    oats = oats_class({'which':'Steel Cut Oats','variants':{'Steel Cut Oats':[{'name':'SCO','cooking_time':42.0}]}})
    assert oats[0].rcp['name'] == 'SCO'
    assert oats[0].rcp['cooking_time'] == 42.0

def test_list():
    rcpf = RecipeFactory(logger=collection_logger)

    oats_class = rcpf.get({'source':'test_recipes/Oats.yml'})
    oats = oats_class({'which':'Oat Medley'})
    assert oats[0].rcp['name'] == 'Steel Cut Oats'
    assert oats[1].rcp['name'] == 'Rolled Oats'
