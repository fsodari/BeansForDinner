from BeansForDinner.Recipe.recipe_factory import RecipeFactory
from BeansForDinner.Recipe import RecipeFactory, import_recipe, export_recipe, sort_recipe_config

def test_export():
    oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    export_file = 'tmp/OatmealExport.yml'
    export_recipe(oatmeal.rcp, export_file)
