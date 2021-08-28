from BeansForDinner.Recipe import RecipeFactory

def test_basic():
    dough = RecipeFactory({'source':'test_recipes/HerndonWholeDough.yml'})

    assert dough.ingredients()['levain'].amount() == 360
    assert dough.ingredients()['flour'].amount() == 800
    assert dough.amount() == 1822.0

def test_imnt():
    dough = RecipeFactory({'source':'test_recipes/HerndonWholeDough.yml'})

    assert dough.iamount('White Flour') == 450.0
    assert dough.iamount('Whole Wheat Flour') == 500.0
    assert dough.iamount('Rye Flour') == 50.0
    assert dough.iamount('Water') == 800.0