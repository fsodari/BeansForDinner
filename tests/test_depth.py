from BeansForDinner.Recipe import RecipeFactory

"""
Using collections within collections is possible, however there is no oppurtunity for the
user to override the 'which' option more than once. They would need to override the lower level collections
by editing the recipes.
"""
def test_collection_levels():
    grains = RecipeFactory({'source':'test_recipes/Grains.yml'})
    assert grains.name() == 'Rollllled Oats'

def test_collection_overrides():
    # Steel contains an override to choose steel cut oats from oats
    grains = RecipeFactory({'which':'Steel', 'source':'test_recipes/Grains.yml'})
    assert grains.name() == 'Steel Cut Oats'