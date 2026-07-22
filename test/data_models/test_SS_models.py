
from pyampacity.standard_thermal_models.class_conditions_weather_site import Conditions_Weather_Site
from pyampacity.standard_thermal_models.class_thermal_model           import Thermal_Model
from pyampacity.standard_thermal_models.class_conductor               import Conductor

from   copy  import deepcopy

def get_models_test_SS(data):

    # generate cigre601 and ieee738 class  
    ###############################################
    conditions = Conditions_Weather_Site().set_data(data) 
    conductor  = Conductor().set_data(data) 
    
    model_cigre = Thermal_Model(standard='CIGRE601')
    model_cigre.set_conditions( deepcopy(conditions) )
    model_cigre.set_conductor(  deepcopy(conductor)  )
    
    model_ieee = Thermal_Model(standard='IEEE738')
    model_ieee.set_conditions( deepcopy(conditions) )
    model_ieee.set_conductor(  deepcopy(conductor)  )
    
    return model_cigre, model_ieee
    