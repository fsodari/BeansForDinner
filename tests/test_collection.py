from BeansForDinner import RecipeFactory

def test_default():
    oats = RecipeFactory({'source':'test_recipes/Oats.yml'})

    assert oats.name() == 'Rollllled Oats'
    # Make sure it's using the class overrides
    assert oats.cooking_time() == 5.0

def test_option():
    # Select a different option. You must override 'which' in the user config now, or else it
    # will use the default option.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml', 'which':'Steel Cut Oats'})

    assert oats.name() == 'Steel Cut Oats'
    assert oats.cooking_time() == 13.0

def test_new():
    # If the choice is not in the collection, default is created.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml', 'which':'Groats'})

    assert oats.name() == 'Steel Cut Oats'

    # Overriding collection with new variants. Do whatever you want. I don't care.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml','which':'Groats','variants':{'Groats':{'name':'Groats','cooking_time':20.0}}})
    
    assert oats.name() == 'Groats'
    assert oats.cooking_time() == 20.0

def test_overrides():
    # Test overriding paramters of recipes in the collection.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml', 'which':'Steel Cut Oats'})

    # Overrides are applied based on the returned class.
    oats.override({'name':'SCO','cooking_time':42.0})

    assert oats.name() == 'SCO'
    assert oats.cooking_time() == 42.0
