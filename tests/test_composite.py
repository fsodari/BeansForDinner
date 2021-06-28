from BeansForDinner import RecipeFactory

def test_composite_basic():
    oatmeal_class = RecipeFactory({'source':'recipe_config/Oatmeal.yml'})
    oatmeal_inst = oatmeal_class()
    assert oatmeal_inst.rcp['name'] == 'Oatmeal'
    print(oatmeal_inst.rcp['ingredients']['base'].rcp['name'])
    assert oatmeal_inst.rcp['ingredients']['base'].rcp['cooking_time'] == 11.1

    # You cannot reuse a class created from RecipeFactory. It must be a new instance.
    oatmeal2 = RecipeFactory({'source':'recipe_config/Oatmeal.yml'})
    oats2 = oatmeal2({'ingredients':{'base':{'source':'recipe_config/RolledOats.yml'}}})
    assert oats2.rcp['name'] == 'Oatmeal'
    assert oats2.rcp['ingredients']['base'].rcp['name'] == 'Rolled Oats'
