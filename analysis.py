#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:44:43 2020

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

#%% Flight 3 Data ingestion

Sound = {'dev4': gf.Sounds(os.path.join(datadir, 'Device 4', 'FileNo3.txt'), ts='2019-06-20T21:00:00')['Sounds'],
         'dev8': gf.Sounds(os.path.join(datadir, 'Device 8', 'FileNo3.txt'), ts='2019-06-20T21:00:00')['Sounds'],
         'devD': gf.Sounds(os.path.join(datadir, 'Device D','FileNo2.txt'), ts='2019-06-20T21:00:00')['Sounds']
         }


Motion = { 'dev4': gf.Motion(os.path.join(datadir, 'Device 4', 'FileNo3.txt'), ts='2019-06-20T21:00:00')['Motion'],
          'dev8': gf.Motion(os.path.join(datadir, 'Device 8', 'FileNo3.txt'), ts='2019-06-20T21:00:00')['Motion'],
          'devD': gf.Motion(os.path.join(datadir, 'Device D','FileNo2.txt'), ts='2019-06-20T21:00:00')['Motion']
          }


info = pd.read_excel(os.path.join(datadir,'FilesFrom418th.xlsx'), sheet_name = 'Flight 3')


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

#%% First set of touch and go

q = "Time > '2019-06-20 22:20:00' & Time < '2019-06-20 22:50:00'"

blah_m = {}
for k in Motion.keys():
    blah_m[k] = roll_m(Motion[k].query(q), 10)


    
blah_s={}
for k in Sound.keys():
    blah_s[k] = roll_s(Sound[k].query(q), 256*10)



#%% Plots
    
blah_m['dev4']['y'].plot();
tg_times = ['2019-06-20 22:25:45','2019-06-20 22:33:28', '2019-06-20 22:42:12', '2019-06-20 22:47:00']
for tg in tg_times:
    plt.axvline(x = tg, color = 'g', linestyle='--');

blah_s['devD'].plot();
tg_times = ['2019-06-20 22:25:45','2019-06-20 22:33:28', '2019-06-20 22:42:12', '2019-06-20 22:47:00']
for tg in tg_times:
    plt.axvline(x = tg, color = 'g', linestyle='--');

#%%
q1 = "Time < '2019-06-21 01:24:00'"
bl = {}
for k in Sound.keys():
    bl[k] = Sound[k].query(q)['Sound']
    bl[k].index = Sound[k].query(q)['Time']
sound_df = pd.DataFrame(bl)
sound_df.plot(subplots=True, layout = (3,1), sharex = True, sharey=False, ylim=(0,3000)) 
sound_df_smooth = sound_df.rolling(window = 256*5, center=True).mean()

sound_df_smooth.plot(subplots=True, layout=(3,1), sharex=True, sharey=False)
