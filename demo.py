from BeansForDinner import RecipeFactory

# Demonstration of the Recipe Factory
if __name__ == '__main__':
    # Atomic recipe example
    # Get a new recipe factory from a yaml template. Neat.
    steel = RecipeFactory({'source':'test_recipes/SteelCutOats.yml'})
    
    print(f"Default SteelCutOats: Name: {steel.rcp['name']}, Cooking Time: {steel.rcp['cooking_time']}")

    # Collection examples.
    # Default.
    oats = RecipeFactory({'source':'test_recipes/Oats.yml'})
    # Collection overrides are applied to base recipe.
    print(f"Oats Collection Rolled Name: {oats.rcp['name']}, Cooking Time: {oats.rcp['cooking_time']}")

    # Use a different option
    oats2 = RecipeFactory({'which':'Steel Cut Oats','source':'test_recipes/Oats.yml'})
    print(f"Oats Collection Steel Cut Name: {oats2.rcp['name']}, Cooking Time: {oats2.rcp['cooking_time']}")

    # Composite Recipe example
    oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Using Composite overrides in file
    print(f"Oatmeal: Name: {oatmeal.rcp['name']}")
    print(f"Oatmeal Base: {oatmeal.rcp['ingredients']['base'].rcp['name']}, Liquid: {oatmeal.rcp['ingredients']['liquid'].rcp['name']}")

    # Use a different ingredient from the oats collection.
    oatmeal2 = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Override the ingredients. Aren't config dicts so simple...ha...
    oatmeal2.override({'ingredients':{'base':{'source':'test_recipes/RolledOats.yml'}}})

    print(f"Oatmeal2 Base: {oatmeal2.rcp['ingredients']['base'].rcp['name']}, Liquid: {oatmeal2.rcp['ingredients']['liquid'].rcp['name']}")
    # This could be implemented in the base class
    total_cook_time = 0
    for k in oatmeal2.rcp['ingredients']:
        total_cook_time += oatmeal2.rcp['ingredients'][k].rcp['cooking_time']
    print(f"Total Cook Time: {total_cook_time}")

    # We can create Composites on-the-fly using a list/tuple
    quinoa_oatmeal = RecipeFactory({'source':'test_recipes/Oatmeal.yml'})
    # Substitute multiple ingredients for one.
    quinoa_oatmeal.override({
        'ingredients':{
            'base':[
                {'source':'test_recipes/SteelCutOats.yml'},
                {'source':'test_recipes/Quinoa.yml'}]
            }})

    print(f"Quinoa Oatmeal Base: {quinoa_oatmeal.rcp['ingredients']['base'].rcp['name']}")
