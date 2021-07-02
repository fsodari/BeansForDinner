from BeansForDinner import RecipeFactory

def test_basic():
    oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})

    assert oatmeal.name() == 'Oatmeal'
    # Make sure the composite overrides were applied.
    assert oatmeal.cooking_time() == 16.1

def test_user_override():
    # Override ingredients in the user config.
    oats = RecipeFactory({'source':'test_recipes/Oatmeal.yml','ingredients':{'base':{'source':'test_recipes/RolledOats.yml'}}})
    
    assert oats.name() == 'Oatmeal'
    assert oats.ingredients()['base'].name() == 'Rolled Oats'

def test_override_later():
    oats = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Override ingredients after the class is initialized.
    oats.override({'ingredients':{'base':{'source':'test_recipes/RolledOats.yml'}}})

    assert oats.name() == 'Oatmeal'
    assert oats.ingredients()['base'].name() == 'Rolled Oats'
