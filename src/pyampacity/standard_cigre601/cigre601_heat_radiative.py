from   pyampacity.utils.utils import check_nans
import numpy as np

def heat_radiative(conductor, conditions):
    """
    Parameters:
    conductor  obj
    conditions obj

    Returns:
    Pr : radiative W/m
    """
    # Stefan-Boltzmann constant W / (m**2 * K**4)
    sigma_B   = 5.670374419e-08 
    Ta        = conditions.air_temperature
    Ts        = conditions.conductor_temperature

    D         = conductor.diameter_D       
    epsilon_s = conductor.emissivity
    
    # radiative heat loss (W/m)
    Pr = np.pi*D*sigma_B*epsilon_s*( (Ts+273)**4 - (Ta+273)**4 )
    
    check_nans(Pr ,txt='Pr')

    return Pr