# Atomic Recipes

Atomic recipes are recipes which reference no other recipes. They are self contained and should provide all instructions, quantities, and information needed to prepare themselves. Atomic recipes should be signular, whole ingredients, or more complex recipes that are obtained as a singular item like store bought ketchup.


Atomic recipes have no actual requirements. If no name is supplied, the filename will be used. The base recipe class will supply any missing fields with defaults.

However, it is best to fill out Atomics with as much information as possible. That way recipes can be scaled accurately and top-level recipes can depend on low level ingredients for details.

    name: Steel Cut Oats
    cooking_time: 14.0  # minutes
    serving_size: 100.0 # grams
