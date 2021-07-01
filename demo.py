from BeansForDinner import RecipeFactory

# Demonstration of the Recipe Factory
if __name__ == '__main__':
    # Atomic recipe example
    # Get a new recipe factory from a yaml template. Neat.
    steel = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})
    
    print(f"Default SteelCutOats: Name: {steel.name()}, Cooking Time: {steel.cooking_time()}")

    # Collection examples.
    # Default.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml'})
    # Collection overrides are applied to base recipe.
    print(f"Oats Collection Rolled Name: {oats.name()}, Cooking Time: {oats.cooking_time()}")

    # Use a different option
    oats2 = RecipeFactory({'which':'Steel Cut Oats','source':'test_recipes/Oats.yml'})
    print(f"Oats Collection Steel Cut Name: {oats2.name()}, Cooking Time: {oats2.cooking_time()}")

    # Composite Recipe example
    oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Using Composite overrides in file
    print(f"Oatmeal: Name: {oatmeal.name()}")
    print(f"Oatmeal Base: {oatmeal.rcp['ingredients']['base'].name()}, Liquid: {oatmeal.rcp['ingredients']['liquid'].name()}")

    # Use a different ingredient from the oats collection.
    oatmeal2 = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Override the ingredients. Aren't config dicts so simple...ha...
    oatmeal2.override({'ingredients':{'base':{'source':'test_recipes/RolledOats.yml'}}})

    print(f"Oatmeal2 Base: {oatmeal2.rcp['ingredients']['base'].name()}, Liquid: {oatmeal2.rcp['ingredients']['liquid'].name()}")
    print(f"Total Cook Time: {oatmeal2.cooking_time()}")

    # We can create Composites on-the-fly using a list/tuple
    quinoa_oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Substitute multiple ingredients for one.
    quinoa_oatmeal.override({
        'ingredients':{
            'base':[
                {'source':'test_recipes/SteelCutOats.yml'},
                {'source':'test_recipes/Quinoa.yml'}]
            }})

    print(f"Quinoa Oatmeal Base: {quinoa_oatmeal.rcp['ingredients']['base'].name()}")
