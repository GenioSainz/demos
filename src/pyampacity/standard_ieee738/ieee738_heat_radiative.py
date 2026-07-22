
from   pyampacity.utils.utils import check_nans

def heat_radiative(conductor, conditions):
    """
    Parameters:
    conductor  obj
    conditions obj

    Returns:
    qr : radiative W/m
    """

    epsilon = conductor.emissivity
    Ts = conditions.conductor_temperature
    Ta = conditions.air_temperature
    D0 = conductor.diameter_D       

    # radiative heat loss (W/m)
    qr = 17.8*D0*epsilon*( ((Ts+273)/100)**4 - ((Ta+273)/100)**4 )
    
    check_nans(qr ,txt='qr')

    return qr