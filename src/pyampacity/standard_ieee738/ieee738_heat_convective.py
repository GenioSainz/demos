from   pyampacity.utils.utils import check_nans, sind, cosd
import numpy as np

def heat_convective(conductor, conditions):
    """
    Parameters:
    conductor  obj
    conditions obj

    Returns:
    qc : convective W/m
    """

    Ta = conditions.air_temperature
    Ts = conditions.conductor_temperature
    He = conditions.altitude
    
    D0  = conductor.diameter_D 
        
    Vw  = conditions.wind_speed
    phi = conditions.wind_angle_attack
    
    # film temperature
    T_film = 0.5*(Ts+Ta) 
    
    # dynamic_viscosity of air (kg ⁄ m−s or N−s ⁄ m^2)
    mu_f = (1.458e-6 * (T_film + 273)**1.5) / (T_film + 383.4)
    
    # air density (kg⁄m^3)   
    rho_f = (np.poly1d([6.379e-9, -1.525e-4, 1.293])(He)) / (1 + 0.00367 * T_film)
  
    # thermal conductivity of air W ⁄ (m × °C)
    k_f = np.poly1d([-4.407e-9, 7.477e-5, 2.424e-2])(T_film)
    
    # Reynolds Number: The equations for forced convection heat loss have an upper limit of application validity of 
    # a Reynolds number of 50 000 which is an order of magnitude higher than overhead transmission line conductors experience.
    N_Re = (D0*rho_f*Vw)/mu_f
    if np.any(N_Re > 50_000):print('*'*50);print('Reynolds number IEEE738 > 50_000 !!!')
    
    # Wind direction factor
    K_angle = 1.194 - cosd(phi) + 0.194 * cosd(2*phi) + 0.368*sind(2*phi)

    # Natural convection q_cn (W/m)
    q_cn = 3.645*rho_f**0.5*D0**0.75*(Ts - Ta) ** 1.25
    
    # Forced convection  (W/m)
    # q_c1: Low  Reynolds number 
    # q_c2: High Reynolds number 
    q_c1 = K_angle*(1.01 + 1.35 * N_Re**0.52)*k_f*(Ts - Ta)
    q_c2 = K_angle*0.754*N_Re**0.6*k_f*(Ts - Ta)
    
    # Result maximum of natural convection and forced convection (W/m)
    ###################################################################
    qc = np.maximum( q_cn, np.maximum(q_c1, q_c2) )
    
    check_nans(qc ,txt='qc')
    
    return qc
    