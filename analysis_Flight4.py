#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 15:22:09 2020

@author: abhijit
"""

#%% Preamble
import os
os.chdir(os.path.expanduser('~/Zansors'))
import zdevice.garfield as gf
import zdevice.zdevice as zd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

datadir = os.path.expanduser('~/Dropbox/Baabi_GarfieldDeviceDataDownload/Cockpit_418thFlightTestSquadron')

#%% Flight 4 Data ingestion

Sound = {'dev4': gf.Sounds(os.path.join(datadir, 'Device 4', 'FileNo4.txt'), ts='2019-07-18T16:30:00')['Sounds'],
         'dev8': gf.Sounds(os.path.join(datadir, 'Device 8', 'FileNo5.txt'), ts='2019-07-18T16:30:00')['Sounds'],
         'devD': gf.Sounds(os.path.join(datadir, 'Device D','FileNo3.txt'), ts='2019-07-18T16:30:00')['Sounds']
         }


Motion = { 'dev4': gf.Motion(os.path.join(datadir, 'Device 4', 'FileNo4.txt'), ts='2019-07-18T16:30:00')['Motion'],
          'dev8': gf.Motion(os.path.join(datadir, 'Device 8', 'FileNo5.txt'), ts='2019-07-18T16:30:00')['Motion'],
          'devD': gf.Motion(os.path.join(datadir, 'Device D','FileNo3.txt'), ts='2019-07-18T16:30:00')['Motion']
          }


info = pd.read_excel(os.path.join(datadir,'FilesFrom418th.xlsx'), sheet_name = 'Flight 4')
event_times = (info[['EventDate','EventStart']].
               astype(str).
               apply(lambda x: ' '.join(x), axis=1).
               to_list())

#%% Functions

def roll_m(d, window=10):
    bl = d[['x','y','z']]
    bl.index = d['Time']
    bl = bl.rolling(window = window, center=True).mean()
    return(bl)

def roll_s(d, window=256):
    bl = d['Sound']
    bl.index = d['Time']
    bl = bl.rolling(window=window, center=True).mean()
    return(bl)

#%% Making DFs
q1 = "Time < '2019-07-19 22:30:00'"
bl = {}; bl2={'x':{},'y':{}, 'z':{}}
for k in Sound.keys():
    bl[k] = Sound[k].query(q1)['Sound']
    bl[k].index = Sound[k].query(q1)['Time']
    bl2['x'][k] = Motion[k].query(q1)['x']
    bl2['x'][k].index = Motion[k].query(q1)['Time']
    bl2['y'][k] = Motion[k].query(q1)['y']
    bl2['y'][k].index = Motion[k].query(q1)['Time']
    bl2['z'][k] = Motion[k].query(q1)['z']
    bl2['z'][k].index = Motion[k].query(q1)['Time']


sound_df = pd.DataFrame(bl)
motion_df = {'x': pd.DataFrame(bl2['x']),
             'y': pd.DataFrame(bl2['y']),
             'z': pd.DataFrame(bl2['z'])}

#%% Plots

sound_df.plot(subplots=True, layout = (3,1), sharex = True, sharey=False, ylim=(0,3000)) 
sound_df_smooth = sound_df.rolling(window = 256*5, center=True).mean()

sound_df_smooth.plot(subplots=True, layout=(3,1), sharex=True, sharey=False)


ax = motion_df['z'].plot(subplots=True, layout=(3,1), sharex=True)
for i, a in enumerate(ax.ravel()):
    for j in range(len(event_times)):
        a.axvline(x = event_times[j], linestyle='--', color='g')



fig, ax = plt.subplots(3,1)
for a in ax:
    a.axvline(x = 0.6, color='g')
    
