from BeansForDinner import RecipeFactory

def test_simple():
    foobar = RecipeFactory([{'name':'Foo'},{'name':'Bar'}])
    assert foobar.rcp['name'] == 'Foo and Bar'
    assert foobar.rcp['ingredients']['Foo'].rcp['name'] == 'Foo'
    assert foobar.rcp['ingredients']['Bar'].rcp['name'] == 'Bar'
