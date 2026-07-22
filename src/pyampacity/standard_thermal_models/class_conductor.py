from dataclasses import dataclass, fields
from typing      import Optional
from copy        import deepcopy

@dataclass
class Conductor:
    
    conductor_name:     Optional[str]   = None

    solar_absorptivity: Optional[float] = None # (dimensionless)
    emissivity:         Optional[float] = None # (dimensionless)

    diameter_D:         Optional[float] = None # conductor diameter (mm) 
    diameter_d:         Optional[float] = None # outer layer strand diameter (mm)
    diameter_c:         Optional[float] = None # core diameter (mm)

    Rac_at_temp1:       Optional[float] = None # (Ω/m) 
    Rac_at_temp2:       Optional[float] = None # (Ω/m)
    temp1_Rac:          Optional[float] = None # (ºC)
    temp2_Rac:          Optional[float] = None # (ºC)
    
    conductor_max_temperature:  Optional[float] = None # (ºC)
    
    beta20_a: Optional[float] = None # Temperature   coefficient of aluminiun specific heat capacity (1/K)
    beta20_s: Optional[float] = None # Temperature   coefficient of steel     specific heat capacity (1/K)
    c20_a:    Optional[float] = None # Specific heat capacity of aluminiun at 20ºC (J/kg*K)
    c20_s:    Optional[float] = None # Specific heat capacity of steel     at 20ºC (J/kg*K)
    ma:       Optional[float] = None # Aluminiun mass per unit length (kg/m)
    ms:       Optional[float] = None # Steel     mass per unit length (kg/m)
    m:        Optional[float] = None # Total     mass per unit length (kg/m)
          
    @classmethod
    def set_data(cls, data): # keep only fields that exist on the dataclass
        data = deepcopy(data)
        dataclass_keys = {f.name for f in fields(cls)}
        keys_filter    = {k: v for k, v in data.items() if k in dataclass_keys}
        return cls(**keys_filter)
            


  
