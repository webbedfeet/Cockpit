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
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import signal

datadir = os.path.expanduser('~/Dropbox/Baabi_GarfieldDeviceDataDownload/Cockpit_418thFlightTestSquadron')

#%% Flight 2 Data ingestion

Sound = {'dev4': gf.Sounds(os.path.join(datadir, 'Device 4', 'FileNo2.txt'), ts='2019-06-12T17:43:00')['Sounds'],
         'dev8': gf.Sounds(os.path.join(datadir, 'Device 8', 'FileNo2.txt'), ts='2019-06-12T17:43:00')['Sounds'],
         'devD': gf.Sounds(os.path.join(datadir, 'Device D','FileNo1.txt'), ts='2019-06-12T17:43:00')['Sounds']
         }


Motion = { 'dev4': gf.Motion(os.path.join(datadir, 'Device 4', 'FileNo2.txt'), ts='2019-06-12T17:43:00')['Motion'],
          'dev8': gf.Motion(os.path.join(datadir, 'Device 8', 'FileNo2.txt'), ts='2019-06-12T17:43:00')['Motion'],
          'devD': gf.Motion(os.path.join(datadir, 'Device D','FileNo1.txt'), ts='2019-06-12T17:43:00')['Motion']
          }


info = pd.read_excel(os.path.join(datadir,'FilesFrom418th.xlsx'), sheet_name = 'Flight 2')


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

def plot_times(times, ax = None):
    if ax is None:
        ax = plt.gca()
    for t in times:
        ax.axvline(x = t, linestyle='--', color = 'g')

def plot_panel(d_s, d_m, channel, int_times):
    mpl.style.use('grayscale')
    f, AX = plt.subplots(nrows=4, ncols=1, sharex = True, num = 'seaborn')
    ylabs = ['Sound','Motion (x)','Motion (y)', 'Motion (z)']
    d_s.plot(y = channel, ax = AX[0], legend=None)
    # AX[0].get_yaxis().set_visible(False)
    AX[0].set_ylabel('Sound')
    plot_times(int_times, ax = AX[0])
    d_m['x'].plot(y = channel, ax=AX[1],legend=None)
    # AX[1].get_yaxis().set_visible(False)
    plot_times(int_times, ax= AX[1])
    d_m['y'].plot(y = channel, ax=AX[2],legend=None)
    # AX[2].get_yaxis().set_visible(False)
    plot_times(int_times, ax = AX[2])
    d_m['z'].plot(y = channel, ax=AX[3],legend=None)
    # AX[3].get_yaxis().set_visible(False)
    plot_times(int_times, ax=AX[3])
    AX[3].set_xlabel('Time')
    f.subplots_adjust(hspace=0)
    for i in range(len(AX)):
        AX[i].set_ylabel(ylabs[i], rotation='horizontal',ha = 'right')
        AX[i].set_yticklabels([])
        AX[i].set_yticks([])
        AX[i].grid(False)

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog = False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b,a=butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b,a,data)
    return y

#%% Making DFs
q1 = "Time > '2019-06-12 19:50:00' & Time < '2019-06-13 02:30:00'"
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
motion_df_smooth = {}
for k in motion_df.keys():
    motion_df_smooth[k] = motion_df[k].rolling(5, center=True).mean()


sound_df_smooth = sound_df.rolling(128, center=True).mean()
# sound_df_smooth.plot(subplots=True, layout=(2,1), sharex = True)

del bl, bl2


#%% First set of touch and go

d_tg_s1 = sound_df_smooth['2019-06-12 22:20:00':'2019-06-13 00:15:00']
d_tg_m1 = {}
for k in motion_df_smooth.keys():
    d_tg_m1[k] = pd.DataFrame(motion_df[k])['2019-06-12 22:20:00':'2019-06-13 00:15:00']

interesting_time = ['22:24:58','22:35:40','23:14:23','23:29:48','23:46:05','23:58:56']
interesting_dt = ['2019-06-12 '+u for u in interesting_time]

plot_panel(d_tg_s1, d_tg_m1, 'devD', interesting_dt)
plot_panel(d_tg_s1, d_tg_m1, 'dev8', interesting_dt)
plot_panel(d_tg_s1, d_tg_m1, 'dev4', interesting_dt)
#%% Plots

tg_times = (info.query('EventName == "Go around at touchdown"').
            filter(items=['EventDate','EventTime']).
            astype(str).
            apply(lambda x: ' '.join(x), axis=1).
            to_list())

blah_m['dev4']['y'].plot();
for tg in tg_times:
    plt.axvline(x = tg, color = 'g', linestyle='--');

blah_s['devD'].plot();
for tg in tg_times:
    plt.axvline(x = tg, color = 'g', linestyle='--');

#%%
q1 = "Time < '2019-06-13 00:15:00'"
bl = {}
for k in Sound.keys():
    bl[k] = Sound[k].query(q1)['Sound']
    bl[k].index = Sound[k].query(q1)['Time']
sound_df = pd.DataFrame(bl)
# sound_df.plot(subplots=True, layout = (3,1), sharex = True, sharey=False, ylim=(0,3000)) 
sound_df_smooth = sound_df.rolling(window = 256*5, center=True).mean()

sound_df_smooth.plot(subplots=True, layout=(3,1), sharex=True, sharey=False)
# for x in tg_times:
#     plt.axvline(x, linestyle='--', color='g')


