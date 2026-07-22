from   scipy.interpolate import PchipInterpolator, Akima1DInterpolator, CubicSpline, interp1d
import numpy as np

D2R = np.pi/180
R2D = 180/np.pi

def wswd_2_uv(ws=2,wd=45):
    # u,v scalar components of the wind vector field
    u = -ws*np.sin(wd*D2R)
    v = -ws*np.cos(wd*D2R)
    return u,v

def uv_2_wswd(u=1,v=2):
    # 0º  N u=0  v=-1
    # 90º E u=-1 v=0
    ws = np.sqrt(u**2+v**2)
    wd = np.mod( np.arctan2(-u,-v)*R2D, 360)
    return ws, wd

def get_angle_attack(wind_d=45,span_d=0):
    # 0º  N u=0  v=-1
    # 90º E u=-1 v=0
    diff = (wind_d-span_d)*D2R
    return np.arcsin( np.abs(np.sin(diff)) ) * R2D

def get_times(date_time):
    Nday   = date_time.timetuple().tm_yday
    hour   = date_time.hour  
    minute = date_time.minute 
    second = date_time.second 
    return Nday, hour, minute, second

def sind(degs): 
    return np.sin(degs*D2R)

def cosd(degs): 
    return np.cos(degs*D2R)

def tand(degs): 
    return np.tan(degs*D2R)

def arcsind(degs): 
    return R2D * np.arcsin(degs)

def arccosd(degs): 
    return R2D * np.arccos(degs)

def arctand(degs): 
    return R2D * np.arctan(degs)
        
def get_interpolators(t, y, mode="Linear"):
        if   mode=='Linear': return interp1d(t, y, kind="linear",   fill_value="extrapolate",  bounds_error=False)
        elif mode=='Step':   return interp1d(t, y, kind="previous", fill_value=(y[0],y[-1]),   bounds_error=False)
        elif mode=='Pchip':  return PchipInterpolator(t, y, extrapolate=True)
        elif mode=='Spline': return CubicSpline(t, y, extrapolate=True)
        elif mode=='Akima':  return Akima1DInterpolator(t, y, extrapolate=True)    
         
        else: raise ValueError("Please enter a correct interpolator name !!!")
        
def eval_interpolator(t, y ,t_interp, mode='Step'):
    interpolator =  get_interpolators(t, y, mode=mode)
    return interpolator(t_interp)

def check_nans(arr,txt=''):
    if np.isnan(arr).any():
       count_nans = np.sum(np.isnan(arr))
       print('*'*50)
       print(f'ERROR !!! {txt} with shape {arr.shape} has {count_nans} nans !!!')

def print_lists(txt_list,L_list): 
    for txt,L in zip(txt_list,L_list):
        print(f'{txt:15s}',[f"{x:8.3f}" for x in L])
        
def print_check_array(n=1025, str='Heat convective', units='W/m', format_s='17s', format_f='10.5f'):
    if not isinstance(n, np.ndarray): print(f'{str:{format_s}} {n   :{format_f}} {units}')
    else                            : print(f'{str:{format_s}} {n:{format_f}} {units} --> shape={n.shape}')      

def print_heat_balance(Pc, Pr, Ps, Pj, Rac, fs='17s'):
    
    print_check_array(n=Pc,  str='Heat convective: ', units='W/m', format_s=fs                  )
    print_check_array(n=Pr,  str='Heat radiative: ',  units='W/m', format_s=fs                  )
    print_check_array(n=Pj,  str='Heat joule: ',      units='W/m', format_s=fs                  )
    print_check_array(n=Ps,  str='Heat solar: ',      units='W/m', format_s=fs                  )
    print_check_array(n=Rac, str='Rac: ',             units='Ω/m', format_s=fs, format_f='14.5e')

n_spaces   = 70
sep_print1 = '*'*n_spaces 
sep_print2 = '*'*n_spaces 

format_s  = '34s'
format_f  = '8.4f'
    
def print_out_SS_Thermal_Rating(Pc, Pr, Ps, Pj, Rac, standard, input=100, output=1025):
    
    print(sep_print1);print(f'STEADY-STATE THERMAL RATING: {standard}');print(sep_print2)
    print_check_array(n=input,  str='INPUT:  steady state temperature: ', units='°C', format_s=format_s, format_f=format_f)
    print_check_array(n=output, str='OUTPUT: steady state current: ',     units='A',  format_s=format_s, format_f=format_f)
    print('');
    print_heat_balance(Pc, Pr, Ps, Pj, Rac);
    print(sep_print1);print('')
     
def print_out_SS_Conductor_Temperature(Pc, Pr, Ps, Pj, Rac, standard, input=1025, output=100):
    
    print(sep_print1);print(f'STEADY-STATE CONDUCTOR TEMPERATURE: {standard}');print(sep_print2)
    print_check_array(n=input,  str='INPUT:  steady state current: ',     units='A',  format_s=format_s, format_f=format_f)
    print_check_array(n=output, str='OUTPUT: steady state temperature: ', units='°C', format_s=format_s, format_f=format_f)
    print('');
    print_heat_balance(Pc, Pr, Ps, Pj, Rac);
    print(sep_print1);print('')
    