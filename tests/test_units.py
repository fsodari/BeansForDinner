from BeansForDinner.Recipe import Units

def test_basics():
    some_unit = Units(1.0, 'g')
    g = some_unit('g')
    mg = some_unit('mg')
    kg = some_unit('kg')
    assert mg == 1000.0
    assert g == 1.0
    assert kg == 0.001

def test_density():
    some_unit = Units(1.0, 'g')
