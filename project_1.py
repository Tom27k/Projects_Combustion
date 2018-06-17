# The following code is based on already created one
# Neccessary modifications for the project were undertaken


import numpy as np
import cantera as ct
import matplotlib.pyplot as plt


#Mechanism used for the process 
gas = ct.Solution('gri30.xml')

Tmin = 1000
Tmax = 2000
Pmin = 101325
Pmax = 405300
fimin = 0.2 
fimax = 2.4

#Number of iterations
npoints = 11
fipoints = 10

s = 0
nt = 100000 
dt = 10**(-6) #time step size

#Data storage
Ti = np.zeros(npoints, 'd')
Pi = np.zeros(npoints, 'd')
fi = np.zeros(fipoints, 'd')
tim = np.zeros(nt, 'd')
temp_cas = np.zeros(nt, 'd')
dtemp_cas = np.zeros(nt-1, 'd')
Autoignition_cas = np.zeros(npoints**2 * fipoints, 'd')
FinalTemp_cas = np.zeros(npoints**2 *fipoints, 'd')

Autoignition_casTemp = np.zeros(npoints, 'd')
FinalTemp_casTemp = np.zeros(npoints, 'd')
Autoignition_casPressure = np.zeros(npoints, 'd')
FinalTemp_casPressure = np.zeros(npoints, 'd')
Autoignition_casFi = np.zeros(fipoints, 'd')
FinalTemp_casFi = np.zeros(fipoints, 'd')


for j in range(npoints):
    Ti[j]=Tmin + (Tmax-Tmin)*j/(npoints-1)
    
    for p in range(npoints):
        Pi[p] = Pmin + (Pmax-Pmin)*p/(npoints-1)
        
        for f in range(fipoints):
            fi[f] = fimin + (fimax-fimin)*f/(fipoints-1)
            no = float(1/fi[f])
            X='CH4:0.5 O2:'+str(no)
            gas.TPX = Ti[j], Pi[p], X #initial temperature, pressure and stoichiometry
            r = ct.IdealGasReactor(gas) # the batch reactor
            sim = ct.ReactorNet([r]) #reactor network consisting of single batch reactor
            time = 0.0 #initial simulation time
            
            #Running the simulation
            for n in range(nt): #loop for nt times steps of dt seconds
                time += dt
                sim.advance(time)
                tim[n] = time
                temp_cas[n] = r.T
                     
            #autoignition time
            Dtmax=[0,0.0]
            for n in range(nt-1):
                dtemp_cas[n] = (temp_cas[n+1] - temp_cas[n])/dt
                if (dtemp_cas[n] > Dtmax[1]):
                    Dtmax[0] = n
                    Dtmax[1] = dtemp_cas[n]
            Autoignition = (tim[Dtmax[0]] + tim[Dtmax[0] + 1])/2.
            Autoignition_cas[s] = Autoignition*1000 
            FinalTemp_cas[s] = temp_cas[nt-1]
            s += 1

#Data for plots
            if Pi[p] == 101325 and fi[f] == 1:
                FinalTemp_casTemp[j] = temp_cas[nt-1]
                Autoignition_casTemp[j] = Autoignition*1000
            if Ti[j] == 1200 and fi[f] == 1:
                FinalTemp_casPressure[p] = temp_cas[nt-1]
                Autoignition_casPressure[p] = Autoignition*1000
            if Pi[p] == 101325 and Ti[j] == 1200:
                FinalTemp_casFi[f] = temp_cas[nt-1]
                Autoignition_casFi[f] = Autoignition*1000

#PLOTS

#Autoign_time(InitialTemp)

plt.plot(1000/Ti,Autoignition_casTemp,'-',color='red')
plt.xlabel(r'Temp [1000/K]',fontsize=20)
plt.ylabel("Ignition time [ms]")
plt.axis([0.5,1.1,0.0,100.0])
plt.grid()
plt.savefig('Autoign_inittemp.png',bbox_inches='tight')



#Autoign_time(pressure)

plt.plot(Pi,Autoignition_casPressure,'-',color='red')
plt.xlabel(r'Pressure [Pa]',fontsize=20)
plt.ylabel("Ignition time [ms]")
plt.axis([100000,410000,0.5,40.0])
plt.grid()
plt.savefig('Autoign_pressure.png',bbox_inches='tight')






