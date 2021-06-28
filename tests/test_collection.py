from BeansForDinner import RecipeFactory

def test_collection_default():
    oats_class = RecipeFactory({'source':'test_recipes/Oats.yml'})
    oats_inst = oats_class()
    assert oats_inst.rcp['name'] == 'rollllled oats'
    # Make sure it's using the class overrides
    assert oats_inst.rcp['cooking_time'] == 5.0

# def test_collection_option():
#     # Select a different option.
#     oats_class = RecipeFactory({'source':'test_recipes/Oats.yml'})
#     oats = oats_class({'which':'Steel Cut Oats'})
#     assert oats.rcp['name'] == 'Steel Cut Oats'
#     assert oats.rcp['cooking_time'] == 13.0

# def test_collection_new():
#     # If the choice is not in the collection, default is created.
#     oats_class = RecipeFactory({'source':'test_recipes/Oats.yml'})
#     oats = oats_class({'which':'Groats'})
#     assert oats.rcp['name'] == 'Steel Cut Oats'

#     # Overriding collection with variant override.
#     oats_class = RecipeFactory({'source':'test_recipes/Oats.yml'})
#     oats = oats_class({'which':'Groats','variants':{'Groats':{'name':'Groats','cooking_time':20.0}}})
#     assert oats.rcp['name'] == 'Groats'
#     assert oats.rcp['cooking_time'] == 20.0

# def test_collection_overrides():
#     # Test overriding paramters of recipes in the collection.
#     oats_class = RecipeFactory({'source':'test_recipes/Oats.yml'})
#     oats = oats_class({'which':'Steel Cut Oats','variants':{'Steel Cut Oats':{'name':'SCO'}}})
#     assert oats.rcp['name'] == 'SCO'
#     assert oats.rcp['cooking_time'] == 13.0
