import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math

q = sp.constants.elementary_charge #elementary charge
epsilon_r = 54 #dielectric constant
epsilon_0 = sp.constants.epsilon_0*1E-2 #permittivity of free space (in F/cm)
V_T = 300*sp.constants.Boltzmann/q #thermal voltage
V_bi = 1.2 #built-in voltage

def IonConcentration(Q_Ion):
    sqrt1 = np.sqrt(1+16*(V_bi/V_T))
    sqrt2 = np.sqrt(1+16*((V_bi-V_app)/V_T))
    return ((8*Q_Ion/(sqrt1-sqrt2))**2)/(q*epsilon_0*epsilon_r*V_T)

def defineDFs(file_seg):
    directory = '/home/xujus/Documents/ASU/Research/CurrentTransients/data/' # will need to change this, this is the firectory to the data files
    file_path = directory + file_seg + ' (Voltage).txt'
    voltage = pd.read_csv(file_path, sep='\\s+', skiprows = 3, dtype={'t (us)': float, 'Vtotal': float, 'Vdev': float}, low_memory=False, names=['t (us)', 'Vtotal', 'Vdev'])
    file_path = directory + file_seg + ' (Current Transients).txt'
    current = pd.read_csv(file_path, sep='\\s+', skiprows = 3, dtype={'t (us)': float, 'J': float, 'Jbimolecular': float}, low_memory=False, names=['t (us)', 'J', 'Jbimolecular'])
    file_path = directory + file_seg + ' (Current Components).txt'
    components = pd.read_csv(file_path, sep='\\s+', skiprows = 3, dtype={'t (us)': float, 'J': float, 'Jn': float, 'Jp': float, 'Janion': float, 'Jcation': float, 'Jdisp': float}, low_memory=False, names=['t (us)', 'J', 'Jn', 'Jp', 'Janion', 'Jcation', 'Jdisp'])
    return [voltage, current, components]

def plotVoltage(df):
    fig, ax = plt.subplots()
    ax.plot(df['t (us)'], df['Vtotal'])
    ax.plot(df['t (us)'], df['Vdev'])
    plt.xlabel('t (us)')
    plt.ylabel('V (V)')
    plt.legend(['Vtotal','Vdev'])
    plt.show()
    
def plotCurrent(df):
    fig, ax = plt.subplots()  
    ax.plot(df['t (us)'], df['J'])
    ax.plot(df['t (us)'], df['Jbimolecular'])
    plt.xlabel('t (us)')
    plt.ylabel('J (mA/cm$^2$)')
    plt.legend(['J','Jbimolecular'])
    plt.show()

def plotComponents(df):
    fig, ax = plt.subplots()
    ax.plot(df['t (us)'], df['J'])
    ax.plot(df['t (us)'], df['Jn'])
    ax.plot(df['t (us)'], df['Jp'])
    ax.plot(df['t (us)'], df['Janion'])
    ax.plot(df['t (us)'], df['Jcation'])
    ax.plot(df['t (us)'], df['Jdisp'])
    plt.xlabel('t (us)')
    plt.ylabel('J components (mA/cm$^2$)')
    plt.legend(['J','Jn','Jp','Janion','Jcation','Jdisp'])
    plt.show()

def findJLow(df):
    J_high = 0
    J_low = 0
    
    for i in range(0,len(df['J'])):
        if(df['J'][i] < df['J'][J_low]):
            J_low = i
    return J_low

def IonAndCharge(J, integrationPoint):
    Q_ion = np.trapezoid(J['J'][integrationPoint:]*1E-3, J['t (us)'][integrationPoint:]*1E-6)
    print("Q_Ion:", Q_ion, "Coulombs/cm^2")
    print("Ions Concentration:", IonConcentration(Q_ion), "Ions/cm^2")


# Load the data file (6 different files)
# current in in mA/cm^2 (times 10^-3 for A/cm^2)
# time is in us (times 1E-4 to convert to seconds)
file_segs = ['Ion Density 1E18 Transient EH 1,5 AC mob 1e6_55',
             'Ion Density 1E18 Transient EH 1,5 AC mob 1e6_longOFF_55',
             'Ion Density 1E18 Transient EH 1,5 AC mob 1e6_longOFF_CatOnly_55',
             'Ion Density 1E18 Transient EH 1,5 AC mob 1e6_longOFF_CatOnly_dopedNiOx_55',
             'Ion Density 1E18 Transient EH 1,5 AC mob 1e6_longOFF_CatOnly_dopedNiOx_HighV_55',
             'Ion Density 1E18 Transient EH 1,5 AC mob 1e6_longOFF_CatOnly_dopedNiOx_HighV_N01e16_55']

print('\n')
for i in range(0,len(file_segs)):
    V, J, J_components = defineDFs(file_segs[i])
    V_app = V.max()['Vtotal']
    # plotVoltage(V)
    plotCurrent(J)
    plotComponents(J_components)
    J_low = findJLow(J)

    print(file_segs[i])
    print("Expected Q_Ion (N0 = 1E18)", (np.sqrt(q*1E18*epsilon_0*epsilon_r*V_T)/8)*(np.sqrt(1+16*(V_bi/V_T))-np.sqrt(1+16*((V_bi-V_app)/V_T))))
    IonAndCharge(J, J_low)
    print('\n')

""" MEETING NOTES 04/16/2025

    TASKS
       - Try impedance simulations again, use this to understand the difference in N0 in the different simulations.
       - Attempt to match lab simulation results (we will have the voltage, dont know doping but we will have a range). Most likely not be doped (or not doped heavily)

    QUESTIONS
       - A longer time scale could solve some discrepency, not all the ions are being extracted. Are we measuring all the ions in the system? try measuring over a longer period of time?
       - what is the true N0 of the system given the measured value?
       - is the last one the N0 = 1E16? (Double check the SETFOS file)
       - What correlation is there between the impedance measurements and the N0 discrepency? (Task 1)
    
    NOTES
       - Low vs high capacitance can change the ions measured. With the wrong capacitance we might just be charging the capacitor affecting the results. Polarization by capacitance. Ideally we want interfaces that block the ions. High capacitance is better according to Daivde?
       - NiOx has high cap
       - C60 has low Cap (more complicated)
"""
