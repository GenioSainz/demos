from pyampacity.standard_cigre601.cigre601_heat_convective import heat_convective as cigre601_heat_convective
from pyampacity.standard_cigre601.cigre601_heat_radiative  import heat_radiative  as cigre601_heat_radiative
from pyampacity.standard_cigre601.cigre601_heat_solar      import heat_solar      as cigre601_heat_solar 
from pyampacity.standard_cigre601.cigre601_heat_joule      import heat_joule      as cigre601_heat_joule
from pyampacity.standard_cigre601.cigre601_heat_joule      import get_Rac         as cigre601_get_Rac

from pyampacity.standard_ieee738.ieee738_heat_convective import heat_convective  as ieee738_heat_convective
from pyampacity.standard_ieee738.ieee738_heat_radiative  import heat_radiative   as ieee738_heat_radiative
from pyampacity.standard_ieee738.ieee738_heat_solar      import heat_solar       as ieee738_heat_solar 
from pyampacity.standard_ieee738.ieee738_heat_joule      import heat_joule       as ieee738_heat_joule 
from pyampacity.standard_ieee738.ieee738_heat_joule      import get_Rac          as ieee738_get_Rac

from pyampacity.utils.utils import get_interpolators
from pyampacity.utils       import utils
import numpy as np
from copy                   import deepcopy

class Thermal_Model():
    
    def __init__(self, standard = "IEEE738"):
        
        self.get_interpolator = get_interpolators
        self.standard   = standard
        self.conditions = None
        self.conductor  = None
        
        match standard:
              case "CIGRE601" : 
                self.get_heat_convective = cigre601_heat_convective
                self.get_heat_radiative  = cigre601_heat_radiative
                self.get_heat_solar      = cigre601_heat_solar 
                self.get_heat_joule      = cigre601_heat_joule
                self.get_Rac             = cigre601_get_Rac
              case "IEEE738"  : 
                self.get_heat_convective = ieee738_heat_convective
                self.get_heat_radiative  = ieee738_heat_radiative
                self.get_heat_solar      = ieee738_heat_solar 
                self.get_heat_joule      = ieee738_heat_joule
                self.get_Rac             = ieee738_get_Rac
              case    _       : 
                raise ValueError("Please enter a correct standard: \n - DLR(standard='IEEE738')\n - DLR(standard='CIGRE601')")
        
    def set_conditions(self, conditions):
        self.conditions = deepcopy(conditions)
        
    def set_conductor(self, conductor):
        self.conductor = deepcopy(conductor)
    
    def get_heat_balance(self):
        Pc  = self.get_heat_convective( self.conductor, self.conditions )
        Pr  = self.get_heat_radiative(  self.conductor, self.conditions )
        Ps  = self.get_heat_solar(      self.conductor, self.conditions )
        Pj  = self.get_heat_joule(      self.conductor, self.conditions )
        return Pc, Pr, Ps, Pj
        
    # STEADY-STATE thermal rating 
    def SS_Thermal_Rating(self, print_out=True):  # Tss --> Iss
        
        # Heat balance
        Pc, Pr, Ps, Pj = self.get_heat_balance()
        

        Rac = self.get_Rac(self.conductor, self.conditions )
        Iss = np.sqrt( (Pr+Pc-Ps)/Rac )
        
        # update current
        self.conditions.conductor_current = Iss

        # Heat balance
        Pc, Pr, Ps, Pj = self.get_heat_balance()
        Rac = self.get_Rac(self.conductor, self.conditions )
        
        if print_out:
           ss_temperature = self.conditions.conductor_temperature
           ss_current     = Iss
           utils.print_out_SS_Thermal_Rating(Pc, Pr, Ps, Pj, Rac, self.standard, input=ss_temperature, output=ss_current )
        
        return Iss
    
    # STEADY-STATE conductor temperature    
    def SS_Conductor_Temperature(self, print_out=True):  # Iss --> Tss

        # Tx assumed conductor temperature
        dT   = self.conditions.dT_SSCT
        Tmin = self.conditions.air_temperature           + 1
        Tmax = self.conductor.conductor_max_temperature  + 100
        Tx   = np.arange(Tmin,Tmax+dT,dT)
        
        # The heat balance is computed for each temperature in the vector Tx 
        self.conditions.conductor_temperature = Tx

        # Heat balance
        Pc, Pr, Ps, Pj = self.get_heat_balance()
        heat_balanece  = Ps + Pj - Pc - Pr
        indx_min       = np.argmin( np.abs(heat_balanece) )
        
        # steady state temperature
        Tss = Tx[indx_min]
                    
        # update temperature
        #################################################
        self.conditions.conductor_temperature = Tss

        ## Heat balance
        Pc, Pr, Ps, Pj = self.get_heat_balance()
        Rac = self.get_Rac(self.conductor, self.conditions )
        
        if print_out:
           ss_temperature = Tss
           ss_current     = self.conditions.conductor_current
           utils.print_out_SS_Conductor_Temperature(Pc, Pr, Ps, Pj, Rac, self.standard, input=ss_current, output=ss_temperature)
                       
        return Tss
    
    def SS_Conductor_Temperature_arr(self, Ws, Wd, Ta, I, IT):  # Iss --> Tss

        Tss_arr = []

        for i in range(Ws.size):

            self.conditions.wind_speed             = Ws[i]  # (m/s)
            self.conditions.wind_angle_attack      = Wd[i]  # angle between conductor axis and wind (deg)
            self.conditions.air_temperature        = Ta[i]  # (°C)
            self.conditions.global_solar_radiation = IT[i]  # (w/m2)
            self.conditions.conductor_current      = I[i]   # (A)
            Tss_arr.append( self.SS_Conductor_Temperature(print_out=False) )
            

        return np.array( Tss_arr )
            
    def get_heat_capacity(self):
        # toal heat capacity of the conductor in function of temperature conductor T
        c_T      = lambda c20, beta20, T: c20*( 1 + beta20*(T-20) )
        beta20_a = self.conductor.beta20_a
        beta20_s = self.conductor.beta20_s
        c20_a    = self.conductor.c20_a
        c20_s    = self.conductor.c20_s
        ma = self.conductor.ma
        ms = self.conductor.ms
        T  = self.conditions.conductor_temperature
        ma = ma*c_T(c20_a, beta20_a, T) 
        ms = ms*c_T(c20_s, beta20_s, T)
    
        return ma + ms

    # TRANSIENT conductor temperature standar
    def TRAN_Conductor_Temperature(self,t_data, Ws, Wd, Ta, I, IT, dt_tran=60, mode="Step", print_out=False):  # Iss --> Tss
        
        t_tran  = np.arange(t_data[0], t_data[-1] + dt_tran, dt_tran)  # (s)
        delta_t = dt_tran
        
        interp_Ws = self.get_interpolator(t_data, Ws, mode=mode)
        interp_Wd = self.get_interpolator(t_data, Wd, mode=mode)
        interp_IT = self.get_interpolator(t_data, IT, mode=mode)
        interp_Ta = self.get_interpolator(t_data, Ta, mode=mode)
        interp_I  = self.get_interpolator(t_data, I,  mode="Step")
         
        T_tran    = np.zeros_like(t_tran).astype(np.float64)
        T_tran[0] = self.conditions.conductor_temperature
        
        for i in range(0,t_tran.size-1):
         
            ti = t_tran[i]
            
            self.conditions.wind_speed             = interp_Ws(ti)  
            self.conditions.wind_angle_attack      = interp_Wd(ti)
            self.conditions.global_solar_radiation = interp_IT(ti)
            self.conditions.conductor_current      = interp_I(ti)   
            self.conditions.air_temperature        = interp_Ta(ti)  
            
            mc = self.get_heat_capacity()
            Pc, Pr, Ps, Pj = self.get_heat_balance()
            delta_T = (Ps + Pj - Pc - Pr) * delta_t /mc
            
            self.conditions.conductor_temperature += delta_T
            
            T_tran[i+1] = self.conditions.conductor_temperature
            
            if print_out:
               p1 = delta_T
               p2 = self.conditions.conductor_temperature
               print(f'{i%10+1:2d} {p1:10.4f} {p2:10.4f}')
            
        data_tran = dict(  Ws = interp_Ws(t_tran), 
                           Wd = interp_Wd(t_tran), 
                           IT = interp_IT(t_tran), 
                           I  = interp_I(t_tran) ,
                           Ta = interp_Ta(t_tran),
                           )  
            
        return t_tran, T_tran, data_tran
    

