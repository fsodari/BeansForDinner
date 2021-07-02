from BeansForDinner.Recipe import RecipeFactory

def test_simple():
    foobar = RecipeFactory([{'name':'Foo'},{'name':'Bar'}])
    assert foobar.name() == 'Foo and Bar'
    assert foobar.ingredients()['0'].name() == 'Foo'
    assert foobar.ingredients()['1'].name() == 'Bar'

def test_collection_tuple():
    oats = RecipeFactory({'which':'Oat Medley', 'source':'test_recipes/Oats.yml'})

    assert oats.name() == 'Oat Medley'

def test_composite_tuple():
    quinoa_oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Tuples or lists work fine.
    quinoa_oatmeal.override({'ingredients':{'base':({'source':'test_recipes/SteelCutOats.yml'}, {'source':'test_recipes/Quinoa.yml'})}})

    assert quinoa_oatmeal.ingredients()['base'].name() == "Steel Cut Oats and Quinoa"

def test_nameless():
    # The smoothie has no named ingredients. Just a list of recipes.
    # The recipe factory should create a composite from the list.
    smoodie = RecipeFactory({'source':'test_recipes/Smoothie.yml'})
    assert smoodie.name() == 'Smoothie'
    assert smoodie.ingredients()['0'].name() == 'Berries'
    assert smoodie.ingredients()['0'].amount() == 1.1
