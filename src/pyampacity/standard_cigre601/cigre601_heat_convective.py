from   pyampacity.utils.utils import check_nans, sind
import numpy as np

def heat_convective(conductor, conditions):
    """
    Parameters:
    conductor  obj
    conditions obj

    Returns:
    Pc : convective W/m
    """

    Ta = conditions.air_temperature
    Ts = conditions.conductor_temperature
    y  = conditions.altitude
    
    D  = conductor.diameter_D 
    d  = conductor.diameter_d 
        
    V     = conditions.wind_speed
    delta = conditions.wind_angle_attack
    
    Vmin  = 1e-2
    V     = np.where(V>Vmin,V,Vmin)
    delta = np.clip(delta,0,90)
    
    # CHECK IF Ta >= Tc
    if np.any(Ta>=Ts):
       raise ValueError(f" ERROR!!! Ta >= Tc    Ta:{Ta} Tc:{Ts}")
    
    # FORCED CONVECTION
    #########################################
    
    # conductor roughness
    Rs = d/(2*(D-d))

    # film temperature
    Tf = 0.5*(Ts+Ta)  

    # thermal conductivity of air       
    lambda_f = 2.368e-2 + 7.23e-5*Tf-2.763e-8*Tf**2

    # air density
    gamma_f = ( 1.2930 - 1.525e-4*y  + 6.379e-9*y**2  )/( 1 + 0.00367*Tf )

    # dynamic viscosity of air at a given temperature
    mu_f = ( 17.239 + 4.635e-2*Tf - 2.030e-5*Tf**2 )*1e-6

    # kinematic viscosity of air
    v_f = mu_f/gamma_f # dynamic_viscosity_of_air / air_density

    # Reynolds number
    Re = V*D/v_f

    Re_max = 4000.0 # Pag 26. Max value for IMPORTANT!!!!
    Re     = np.where(Re<Re_max, Re, Re_max)

    # compute B,n parameters function of Reynolds and conductor roughness
    B = np.where(Re <= 2650, 0.641, np.where(Rs <= 0.05, 0.178, 0.048))
    n = np.where(Re <= 2650, 0.471, np.where(Rs <= 0.05, 0.633, 0.800))

    # Nusselt number angle attack 90º
    Nu_90 = B*Re**n

    Nu_delta = Nu_90 * np.where(delta<24,
                                ( 0.42 + 0.68*( sind(delta) )**1.08 ),
                                ( 0.42 + 0.58*( sind(delta) )**0.90 ))

    # Forced convection heat
    Pc_forced = np.pi*lambda_f*(Ts-Ta)*Nu_delta
    
    # NATURAL CONVECTION
    #########################################
    Table5 = np.array([[0,    1e2,  1.02 , 0.148],
                       [1e2 , 1e4,  0.850, 0.188],
                       [1e4 , 1e7,  0.480, 0.250],
                       [1e7 , 1e12, 0.125, 0.333],
                       [1e12, 1e20, 0.125, 0.333]]) 
    # Grashof number
    g  = 9.81
    Gr = ( D**3 * (Ts-Ta) * g ) / ( (Tf+273)*v_f**2 )
    
    # Prandtl number
    c_f  = 1005 # Specific Heat Capacity kJ/kgK of air
    Pr   = c_f * mu_f/lambda_f
    GrPr = Gr*Pr
    
    # computed A,m from Table 5
    ind   = np.searchsorted( Table5[:,0], GrPr , side='right')-1
    A     = Table5[ind,2]
    m     = Table5[ind,3]

    # Nusselt number
    Nu_nat = A*(GrPr)**m
    
    # Natural convection heat
    Pc_nat = np.pi*lambda_f*(Ts-Ta)*Nu_nat
    
    # Result maximum of natural convection and heat convection
    ###############################################################
    Pc = np.maximum(Pc_forced,Pc_nat)  # convective heat loss (W/m)
    
    check_nans(Pc ,txt='Pc')
 
    return Pc
    