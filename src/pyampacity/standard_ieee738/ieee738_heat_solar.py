
from   pyampacity.utils.utils import check_nans, sind, cosd, tand, arcsind, arccosd, arctand, get_times
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
    
    He   = conditions.altitude  # height above sea level (m)
    Lon  = conditions.longitude # longitude (deg)
    Lat  = conditions.latitude  # latitude  (deg)
    
    Z1    = conditions.span_azimuth      # azimuth of span (positive from south through west) (deg)
    alpha = conductor.solar_absorptivity # solar absorptivity of conductor surface (dimensionless)
    A     = conductor.diameter_D         # diameter of circle circumscribing the conductor (m)
    Ns    = conditions.clearness_ratio   # clearness ratio (dimensionless)
 
    if  conditions.mode_solar_radiation_data:
        I_T = conditions.global_solar_radiation
        qs  = alpha * I_T * A
        return qs
    else:
        
        # hour angle of the sun
        W = 15 * (-12 + hour + minute/60 + second/3600 + Lon/15)
        W = np.clip( W, -180, 180)
        
        # solar declination
        delta = 23.45*sind(360*(284 + Nday)/365)

        # solar altitude
        Hc = arcsind( cosd(Lat)*cosd(delta)*cosd(W) + sind(Lat)*sind(delta) )
        Hc = np.where(Hc>=0,Hc,0)
        
        # solar azimuth variable
        X  = sind(W) / ( sind(Lat)*cosd(W) - cosd(Lat)*tand(delta) )
        
        # solar azimuth constant
        C = np.where(W<0, np.where( X>=0, 0  , 180),
                          np.where( X>=0, 180, 360), )
        
        # solar azimuth angle
        Zc = C + arctand( X )
        
        Ns = 0
        column = np.where(Ns<0.5,0,1)
        
        # atmosphere     clear      industrual
        Coeff_Hc = [[-42.23910000, 53.1820000],  # A Hc**0
                    [ 63.80440000, 14.2110000],  # B Hc**1
                    [ -1.92200000,  6.6138e-1],  # C Hc**2
                    [  3.46921e-2, -3.1658e-2],  # D Hc**3
                    [ -3.61118e-4,  5.4654e-4],  # E Hc**4
                    [  1.94318e-6, -4.3446e-6],  # F Hc**5
                    [ -4.07608e-9,  1.3236e-8],] # G Hc**6
        
        Coeff_He = [[+1.000000],  # A He**0
                    [+1.148e-4],  # B He**1
                    [-1.108e-8],] # C He**2
        
        Ksolar = np.poly1d( np.flipud( Coeff_He )          .flatten())(He)
        Qs     = np.poly1d( np.flipud( Coeff_Hc )[:,column].flatten())(Hc)
        Qse    = Ksolar*Qs
        
        theta = arccosd( cosd(Hc)*cosd(Zc-Z1) )
        qs    = alpha*Qse*sind(theta)*A
        
        check_nans(qs ,txt='qs')
        
        return np.where(Hc>0, qs, 0)
    
    
    
    
