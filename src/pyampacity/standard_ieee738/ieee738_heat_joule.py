from pyampacity.utils.utils import check_nans

def get_Rac(conductor, conditions):
    
    temp1 = conductor.temp1_Rac
    temp2 = conductor.temp2_Rac
    
    Rac1  = conductor.Rac_at_temp1
    Rac2  = conductor.Rac_at_temp2
    
    T     = conditions.conductor_temperature

    m    = (Rac2-Rac1)/(temp2 - temp1)
    RacT = Rac1 + m*(T-temp1)
    
    return RacT

def heat_joule(conductor, conditions):
    """
    Parameters:
    conductor  obj
    conditions obj

    Returns:
    qj : joule W/m
    """
    Rac = get_Rac(conductor, conditions)
    I   = conditions.conductor_current
    qj  = Rac * I**2
    
    check_nans(qj ,txt='qj')
    
    return qj
