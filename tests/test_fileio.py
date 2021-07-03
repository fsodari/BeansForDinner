from BeansForDinner.Recipe import RecipeFactory

def test_export():
    oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    oatmeal.export('tmp/OatmealExport.yml')
