from BeansForDinner import RecipeFactory

# Demonstration of the Recipe Factory
if __name__ == '__main__':
    # Atomic recipe example
    # Get a new recipe factory from a yaml template. Neat.
    steel_class = RecipeFactory('recipe_config/SteelCutOats.yml')
    # Get an instance of the recipe
    steel_inst = steel_class()
    
    print(f"Default SteelCutOats: Name: {steel_inst.name()}, Cooking Time: {steel_inst.cooking_time()}")

    # Collection example.
    oats_coll = RecipeFactory('recipe_config/Oats.yml')
    # Get instances of the class.
    oats_inst = oats_coll() # Default option
    oats_inst2 = oats_coll('RolledOats')
    print(f"Oats Collection SCO Name: {oats_inst.name()}, Cooking Time: {oats_inst.cooking_time()}")
    print(f"Oats Collection Rolled Name: {oats_inst2.name()}, Cooking Time: {oats_inst2.cooking_time()}")

    # Composite Recipe example
    oatmeal_comp = RecipeFactory('recipe_config/Oatmeal.yml')
    # Using default arguments
    oatmeal_inst = oatmeal_comp()
    print(f"Oatmeal: Name: {oatmeal_inst.name()}")
    print(f"Oatmeal Base: {oatmeal_inst.ingredients['base'].name()}, Liquid: {oatmeal_inst.ingredients['liquid'].name()}")

    # Use a different ingredient from the oats collection
    oatmeal_inst2 = oatmeal_comp({'base':oats_coll('RolledOats')})

    print(f"Oatmeal2 Base: {oatmeal_inst2.ingredients['base'].name()}, Liquid: {oatmeal_inst2.ingredients['liquid'].name()}")
    # This could be implemented in the base class
    total_cook_time = 0
    for i in oatmeal_inst.ingredients:
        total_cook_time += oatmeal_inst.ingredients[i].cooking_time()
    print(f"Total Cook Time: {total_cook_time}")
