from BeansForDinner import RecipeFactory
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='logs/recipe_factory.log', encoding='utf-8', level=logging.DEBUG)
    rcpf_logger = logging.getLogger('RecipeFactoryLogger')

    rcpf = RecipeFactory(logger=rcpf_logger)

    quinoa_class = rcpf.get({'source':'test_recipes/Quinoa.yml'})
    quinoa = quinoa_class()
    