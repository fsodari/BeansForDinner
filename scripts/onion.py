import sys
sys.path.append("../BeansForDinner")
from BeansForDinner import Recipe

class Onion(Recipe):
    def __init__(self, name, type='yellow'):
        Recipe.__init__(self, name)
        self.type = type
