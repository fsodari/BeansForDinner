from BeansForDinner import RecipeFactory

def test_basic():
    steel_class = RecipeFactory('recipe_config/SteelCutOats.yml')
    steel_inst = steel_class()
    assert steel_inst.name() == 'Steel Cut Oats'
