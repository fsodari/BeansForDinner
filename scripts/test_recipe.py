import sys
sys.path.append("../BeansForDinner")
from BeansForDinner import Recipe

if __name__ == '__main__':
    foo = Recipe('foo')
    print(foo.name)