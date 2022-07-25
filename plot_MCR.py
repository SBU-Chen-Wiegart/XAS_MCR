# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:30:21 2022

Plot MCR results from XView stored in json file
Assumes one MCR fit per file

@author: clark
"""
#%% setup
import json
import numpy as np
import matplotlib.pyplot as plt

IN_PATH = r'C:/Users/clark/OneDrive - Stony Brook University/Documents/Karen/MCR'
FILE = 'Model10.json'

#%% organize project data
with open(f'{IN_PATH}/{FILE}', 'r') as mcr_proj:
    model = json.load(mcr_proj)
    
fit_results = model[-1]['data']
dataset = fit_results['dataset']['data']
initial_spectra = fit_results['refset']['data']
refined_spectra = fit_results['data_ref_fit']
refined_conc = fit_results['c_fit']
data_fit = fit_results['data_fit']

full_energies = np.array(dataset['x'])
crop_energies = np.array(refined_spectra['x'])

D = np.array(dataset['data'])
S_guess = initial_spectra  # dictionary with ref spectra names as keys
S_fit = np.array(refined_spectra['data_ref_fit'])
C_fit = np.array(refined_conc['c_fit'])
D_fit = np.array(data_fit['data_fit'])

times = np.genfromtxt(f'{IN_PATH}/Electrochemical_time_points.txt', skip_header=2)
discharge_time_ind = [0, 4, 10, 19, 30, 43]
charge_time_ind = [2, 8, 13, 24, 39]

#%% plot results
plt.rc('axes', labelsize=12, titlesize=14)

plt.plot(full_energies, D, c='k', alpha=0.5)
plt.plot(crop_energies, D_fit, c='r', alpha=0.5)
plt.xlim([crop_energies.min(), crop_energies.max()])
plt.xlabel('$Energy$ $(eV)$')
plt.ylabel('$\mu(E)$')
plt.title('Data vs Fitted Result')
plt.show()

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

for c, rs in zip(colors, S_guess):
    plt.plot(S_guess[rs]['x'], S_guess[rs]['data'], ls='--', c=c, alpha=0.75)
plt.xlim([crop_energies.min(), crop_energies.max()])
plt.xlabel('$Energy$ $(eV)$')
plt.ylabel('$\mu(E)$')

for c, s in zip(colors, S_fit.T):
    plt.plot(crop_energies, s, c=c)
plt.xlim([crop_energies.min(), crop_energies.max()])
plt.xlabel('$Energy$ $(eV)$')
plt.ylabel('$\mu(E)$')
plt.title('Initial vs Fitted Spectra')
plt.show()

for i in discharge_time_ind:
    plt.axvline(times[i], c='c', ls='--', alpha=0.5)
for j in charge_time_ind:
    plt.axvline(times[j], c='r', ls='--', alpha=0.5)
for c in C_fit:
    plt.plot(times, c)
plt.ylim([0,1])
plt.xlabel('$Time$ $(hours)$')
plt.title('Fitted Concentration Profiles')
plt.show()