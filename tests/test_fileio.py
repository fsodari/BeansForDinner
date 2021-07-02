from BeansForDinner.Recipe.recipe_factory import RecipeFactory

def test_export():
    oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    oatmeal.export('tmp/OatmealExport.yml')
