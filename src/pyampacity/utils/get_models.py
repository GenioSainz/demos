from pyampacity.standard_thermal_models.class_conditions_weather_site import Conditions_Weather_Site
from pyampacity.standard_thermal_models.class_thermal_model           import Thermal_Model
from pyampacity.standard_thermal_models.class_conductor               import Conductor

from   datetime import datetime
from   pathlib  import Path
import pandas   as pd

#  'LA125-Penguin', 
#  'LA175-Ostrich', 
#  'LA280-Hawk', 
#  'Drake',
#  'LA455-Condor', 
#  'LA545-Cardinal', 
#  'LA635-Finch',

def get_conductor_data(conductor_name):
    
    current_script_dir = Path(__file__).resolve().parent
    csv_path           = current_script_dir.parent / 'data' / 'data_ACSR_metric.csv'
    
    df_metric = pd.read_csv(csv_path )
    get_value = lambda var_name: df_metric[df_metric["Code"] == conductor_name][var_name].iloc[0]

    return dict(  conductor_name = conductor_name,
                  solar_absorptivity = 0.8,
                  emissivity         = 0.8,
                  Rac_at_temp1   = get_value(var_name="R25")/1000,
                  Rac_at_temp2   = get_value(var_name="R75")/1000,
                  temp1_Rac      = 25,
                  temp2_Rac      = 75,
                  diameter_c     = get_value(var_name="D_c" )/1000,
                  diameter_d     = get_value(var_name="d_AL")/1000,
                  diameter_D     = get_value(var_name="D"   )/1000,
                  beta20_s       = 1.0e-4, 
                  beta20_a       = 3.8e-4,
                  c20_s          = 481, # IEEE  476
                  c20_a          = 897, # IEEE  955
                  ms             = get_value(var_name="W_ST")/1000,
                  ma             = get_value(var_name="W_AL")/1000, 
                  m              = get_value(var_name="W_T" )/1000, 
                  conductor_max_temperature=100,
                ) 


def get_conditions_data(): # for init the weather conditions with CIGRE example
    
    return dict( date_time          = datetime(year=2025,month=6, day=10,hour=11,minute=0,second=0),
                 solar_absorptivity = 0.8,
                 emissivity         = 0.8,
                 altitude           = 0,
                 latitude           = 30,
                 longitude          = 0,
                 span_azimuth       = 90,
                 span_inclination   = 0,
                 clearness_ratio    = 1.0,
                 ground_albedo      = 0.1,
                 wind_angle_attack  = 60.0,
                 wind_speed         = 0.61,
                 air_temperature    = 40.0,
                 conductor_max_temperature = 100,
                 conductor_temperature     = 100,
                 conductor_current         = 976,
                 )
 
    
def get_models_obj( standard="CIGRE601", conductor_name="Drake"):
    
    # standard="CIGRE601", conductor_name="LA280-Hawk"
    # standard="IEEE738",  conductor_name="LA455-Condor"
    
    conductor_data  = get_conductor_data( conductor_name )
    conditions_data = get_conditions_data()
    
    conditions_obj = Conditions_Weather_Site().set_data( conditions_data ) 
    conductor_obj  = Conductor()              .set_data( conductor_data  ) 
    
    model = Thermal_Model( standard=standard )
    model.set_conditions(  conditions_obj    )
    model.set_conductor(   conductor_obj     )
    
    return model