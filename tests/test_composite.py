from BeansForDinner import RecipeFactory

def test_basic():
    oatmeal_class = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    oatmeal_inst = oatmeal_class()
    assert oatmeal_inst.rcp['name'] == 'Oatmeal'
    print(oatmeal_inst.rcp['ingredients']['base'])
    assert oatmeal_inst.rcp['ingredients']['base'][0].rcp['cooking_time'] == 11.1

    # # You cannot reuse a class created from RecipeFactory. It must be a new instance.
    # oatmeal2 = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # oats2 = oatmeal2({'ingredients':{'base':[{'source':'test_recipes/RolledOats.yml'}]}})
    # assert oats2.rcp['name'] == 'Oatmeal'
    # assert oats2.rcp['ingredients']['base'][0].rcp['name'] == 'Rolled Oats'

# def test_list():
#     oatmeal_class = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
#     quinoa_oatmeal = oatmeal_class({'ingredients':{'base':[{'source':'test_recipes/SteelCutOats.yml'},{'source':'test_recipes/Quinoa.yml'}]}})
#     assert quinoa_oatmeal.rcp['name'] == 'Oatmeal'
#     assert quinoa_oatmeal.rcp['ingredients']['base'][0].rcp['name'] == 'Steel Cut Oats'
#     assert quinoa_oatmeal.rcp['ingredients']['base'][1].rcp['name'] == 'Quinoa'

# def test_list_source():
#     oat_salad_class = RecipeFactory({'source':'test_recipes/OatSalad.yml'})
#     oat_salad = oat_salad_class()
#     assert oat_salad.rcp['name'] == 'Oat Salad'
#     assert oat_salad.rcp['ingredients']['base'][0].rcp['name'] == 'Rolled Oats'
#     assert oat_salad.rcp['ingredients']['base'][1].rcp['name'] == 'Steel Cut Oats'
