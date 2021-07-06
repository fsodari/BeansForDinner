# Need to be able to translate units.
standard_unit = 'g'
standard_volume_unit = 'ml'
mass_units = ['mg', 'g', 'kg']
volume_units = ['ml', 'l']

# Scale factors convert the unit to its respective standard unit.
scale_factors = {'mg':1e-03, 'g':1.0, 'kg':1e03}

def from_standard_unit(amount:float, o_unit:str) -> float:
    """Convert an amount in the standard unit to a new unit."""
    return amount / scale_factors[o_unit]

def to_standard_mass(amount:float, i_unit:str):
    return amount * scale_factors[i_unit]

def to_standard_volume(amount:float, i_unit:str):
    return amount * scale_factors[i_unit]

def to_standard_unit(amount:float, i_unit:str) -> float:
    """Convert given unit to the standard unit"""
    return amount * scale_factors[i_unit]

def density_calc(mass:float, mass_units:str, volume:float, volume_units:str):
    """
    Returns the density in standard units.
    inputs should be tuples mass=(amount:float, unit:'str')
    """
    std_mass = to_standard_mass(mass, mass_units)
    std_volume = to_standard_volume(volume, volume_units)
    # Density normalized to standard units
    return std_mass / std_volume

class Units:
    def __init__(self, amount:float=0.0, unit:str='g', density:float=1.0) -> None:
        """Creates a unit instance."""
        # Must use valid inputs.
        if unit not in mass_units and unit not in volume_units:
            err_str = f"'{unit}' is not a valid unit."
            raise ValueError(err_str)

        self._amount = amount
        self._unit = unit
        self._density = density

    def __call__(self, o_unit:str) -> float:
        """Return the amount in the requested unit."""
        std_amt = to_standard_unit(self._amount, self._unit)
        return from_standard_unit(std_amt, o_unit)

 