from   dataclasses import dataclass, fields
from   typing      import Optional
from   copy        import deepcopy

@dataclass
class Conditions_Weather_Site:
      
    # time
    date_time: Optional[float] = None

    # location
    altitude:  Optional[float] = None # (m)
    latitude:  Optional[float] = None # (deg)
    longitude: Optional[float] = None # (deg)
    
    # span_inclination inclination angle respect to the horizontal
    # span_azimuth orientation, (deg) positive from north to east, 0º north, 90º east
    span_inclination: Optional[float] = None 
    span_azimuth:     Optional[float] = None

    # weather conditions 
    mode_solar_radiation_data: Optional[bool]  = False
    global_solar_radiation:    Optional[float] = None # global solar radiation (W/m^2)
    
    air_temperature:    Optional[float] = None  # (°C)
    wind_direction:     Optional[float] = None  # (deg)
    wind_speed:         Optional[float] = None  # (m/s)
    wind_angle_attack:  Optional[float] = None  # angle between conductor axis and wind (deg)
    
    # surface
    clearness_ratio: Optional[float] = None # (dimensionless)
    ground_albedo:   Optional[float] = None # (dimensionless)
    
    # DLR params
    conductor_temperature: Optional[float] = None # (°C)
    conductor_current:     Optional[float] = None # (A)
    
    # Param for computing Steady State Conductor Temperature 
    # SS_Conductor_Temperature
    dT_SSCT: Optional[float] = 0.1
    
    @classmethod
    def set_data(cls, data): # keep only fields that exist on the dataclass
        data = deepcopy(data)
        dataclass_keys = {f.name for f in fields(cls)}
        keys_filter    = {k: v for k, v in data.items() if k in dataclass_keys}
        return cls(**keys_filter)
        