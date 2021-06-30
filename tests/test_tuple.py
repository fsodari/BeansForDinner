from BeansForDinner import RecipeFactory

def test_simple():
    foobar = RecipeFactory([{'name':'Foo'},{'name':'Bar'}])
    assert foobar.rcp['name'] == 'Foo and Bar'
    assert foobar.rcp['ingredients']['Foo'].rcp['name'] == 'Foo'
    assert foobar.rcp['ingredients']['Bar'].rcp['name'] == 'Bar'

def test_collection_tuple():
    oats = RecipeFactory({'which':'Oat Medley', 'source':'test_recipes/Oats.yml'})

    assert oats.rcp['name'] == 'Steel Cut Oats and Rolled Oats'

def test_composite_tuple():
    quinoa_oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Tuples or lists work fine.
    quinoa_oatmeal.override({'ingredients':{'base':({'source':'test_recipes/SteelCutOats.yml'}, {'source':'test_recipes/Quinoa.yml'})}})

    assert quinoa_oatmeal.rcp['ingredients']['base'].rcp['name'] == "Steel Cut Oats and Quinoa"
