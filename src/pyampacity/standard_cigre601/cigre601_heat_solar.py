
from   pyampacity.utils.utils import check_nans, sind, cosd, arcsind, arccosd, get_times
import numpy as np

def heat_solar(conductor, conditions):
    """
    Parameters:
    conductor  obj
    conditions obj

    Returns:
    Ps : solar W/m
    """
    
    Nday, hour, minute, second = get_times(conditions.date_time)
    
    y    = conditions.altitude  # height above sea level (m)
    lon  = conditions.longitude # longitude (deg)
    phi  = conditions.latitude  # latitude  (deg)
    
    Ns   = conditions.clearness_ratio  # clearness ratio (dimensionless)
    F    = conditions.ground_albedo    # albedo (reflectance) of surface (dimensionless)
    
    gamma_c = conditions.span_azimuth      # azimuth of span (positive from south through west) (deg)
    alpha_S = conductor.solar_absorptivity # solar absorptivity of conductor surface (dimensionless)
    D       = conductor.diameter_D         # diameter of circle circumscribing the conductor (m)
 
    if  conditions.mode_solar_radiation_data:
        I_T = conditions.global_solar_radiation
        Ps = alpha_S * I_T * D
        return Ps
    
    else:

        # declination
        delta_S = 23.3*np.sin(2*np.pi*(284 + Nday)/365)

        # hour angle of the Sun
        Z = 15 * (-12 + hour + minute/60 + second/3600 + lon/15)

        # solar altitude
        Hs = arcsind( sind(phi) * sind(delta_S) + cosd(phi) * cosd(delta_S) * cosd(Z) )

        # solar azimuth
        gamma_s = -arcsind( cosd(delta_S) * sind(Z) / cosd(Hs))

        # angle of the solar beam with respect the axis of the conductor
        eta = arccosd(cosd(Hs) * cosd(gamma_s - gamma_c))

        # direct (beam) solar radiation intensity at y=0 (W/m2)
        I_B0 = Ns * (1280 * sind(Hs)) / (sind(Hs) + 0.314)

        # direct (beam) solar radiation intensity at y (W/m2)
        IBy = I_B0 * (1 + 1.4e-4 * y * (1367 / I_B0 - 1))

        # the diffuse solar radiation intensity (W/m2)
        Id = (430.5 - 0.3288 * IBy) * sind(Hs)

        # total solar radiation intensity
        Fpi2 = F*np.pi/2
        I_T  = IBy * (sind(eta) + Fpi2 * sind(Hs)) + Id * (1 + Fpi2)

        # solar heat gain (W/m)
        Ps = alpha_S * I_T * D
        
        check_nans(Ps ,txt='Ps')

        return np.where(Hs>0,Ps,0)
    
    
    
    
