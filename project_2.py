# The following code is based on already created one
# Neccessary modifications for the project were undertaken

import SDToolbox as sd
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt


#initial conditions
P1=ct.one_atm
T1=500
mech = 'wang_highT.cti'

CJ=[]   
P=[]
T=[]
P0=np.linspace(0.5,10,30)*ct.one_atm
T0=np.linspace(300,1000,30)    
fi=np.linspace(0.05,0.65,50)

for t in T0:
    x= 0.5
    n = x/(1-x)
    q ='O2:1.0, CH4:' + str(n)
    [cj_speed,R2] = sd.CJspeed(P1, t, q, mech, 0)  
    gas = sd.PostShock_eq(cj_speed, P1, t, q, mech)
    P.append(gas.P/ct.one_atm)
    T.append(gas.T)
    CJ.append(cj_speed)

plt.plot(T0,CJ)
plt.xlabel('Initial temperature [K]')
plt.ylabel('CJ speed [m/s]')
plt.savefig('cjspeed_temp')
plt.close()

#for p in P0:
#    x= 0.5
#    n = x/(1-x)
#    q ='O2:1.0, CH4:' + str(n)
#    [cj_speed,R2] = sd.CJspeed(p, T1, q, mech, 0)  
#    gas = sd.PostShock_eq(cj_speed, p, T1, q, mech)
#    P.append(gas.P/ct.one_atm)
#    T.append(gas.T)
#    CJ.append(cj_speed)
#
#plt.plot(P0/ct.one_atm,CJ)
#plt.xlabel('Initial pressure [bar]')
#plt.ylabel('CJ speed [m/s]')
#plt.savefig('cjspeed_pres')
#plt.close()


     
#for x in fi:
#    n = x/(1-x)
#    q ='O2:1.0, CH4:' + str(n)
#    [cj_speed,R2] = sd.CJspeed(P1, T1, q, mech, 0)  
#    gas = sd.PostShock_eq(cj_speed, P1, T1, q, mech) 
#    P.append(gas.P/ct.one_atm)
#    T.append(gas.T)
#    CJ.append(cj_speed)
   
#plt.plot(fi*100,CJ)
#plt.xlabel('Concentration [%]')
#plt.ylabel('CJ speed [m/s]')
#plt.savefig('cjspeed')
#plt.close()
