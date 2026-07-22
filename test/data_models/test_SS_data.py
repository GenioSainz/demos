from   datetime import datetime
import numpy as np

def get_data_test_SS(MODE=0):
    
    # 'Example A'     MODE = 0 CIGRE601 Annex E1 E2
    # 'Example B'     MODE = 1 CIGRE601 Annex E1 E2
    # 'random  data'  MODE = 2
    #  4.6.1-4.6.2    MODE = 3 IEEE738  Anenex 4.6.1 and 4.6.2 is almost equal as CIGRE Annex E1 E2 Example A
    
    date_A = datetime(year=2025,month=6, day=10,hour=11,minute=0,second=0)
    date_B = datetime(year=2025,month=10,day=3 ,hour=14,minute=0,second=0)
    date_R = datetime(year   = 2025,
                      month  = np.random.randint(1, 13),
                      day    = np.random.randint(1, 29),   # safe for all months
                      hour   = np.random.randint(0, 24),
                      minute = np.random.randint(1, 60),
                      second = np.random.randint(1, 60))
    
    rand_conductor_temperature = np.random.randint(50,  111)
    rand_conductor_current     = np.random.randint(500, 1201)
    
    data = dict(    conductor_name = ['Drake'],
                    date_time      = [date_A, date_B, date_R],
                    Rac_at_temp1   = [7.283e-5],
                    Rac_at_temp2   = [8.688e-5],
                    temp1_Rac      = [25],
                    temp2_Rac      = [75],
                    
                    diameter_D = [28.14/1000],
                    diameter_d = [4.440/1000],
                    
                    beta20_s = [1.0e-4], 
                    beta20_a = [3.8e-4],
                    c20_s    = [481],
                    c20_a    = [897],
                    ms       = [0.5119],
                    ma       = [1.1160], 
                    m        = [1.6279],

                    solar_absorptivity = [0.8, 0.9, np.round(np.random.rand(),2) ],
                    emissivity         = [0.8, 0.9, np.round(np.random.rand(),2) ],
                    
                    altitude  = [0,  500, np.random.randint(0, 2000)],
                    latitude  = [30, 50 , np.random.randint(0, 40)  ],
                    longitude = [0 , 0  , np.random.randint(-10,20) ],
                    
                    span_azimuth     = [90, 0  , 0],
                    span_inclination = [0,  10 , 0],

                    clearness_ratio = [1.0, 0.50, np.round(np.random.rand(),2) ],
                    ground_albedo   = [0.1, 0.15, np.round(np.random.rand(),2) ],


                    wind_angle_attack = [60.0, 80.0, np.random.randint(0, 85)],
                    wind_speed        = [0.61, 1.66, np.round(np.random.rand()*10,2)],
                    air_temperature   = [40.0, 20.0, np.random.randint(5, 41)],

                    conductor_max_temperature = [100, 100,  rand_conductor_temperature],
                    conductor_temperature     = [100, 100,  rand_conductor_temperature],
                    conductor_current         = [976, 1504, rand_conductor_current    ],
         )
    
    data_new = {}
    filter   = False
    for k, v in data.items():
        if MODE==3:
           filter = True
           MODE   = 0
        if   len(v)==1: data_new[k]=v[0]
        else:           data_new[k]=v[MODE]
        
    # IEE738 4.6.1 and 4.6.2 is almost equal as CIGRE Annex E1 E2 Example A
    if filter:
       data_new["conductor_current"] = 1000
       data_new["wind_angle_attack"] = 90
       
    return data_new
    


    