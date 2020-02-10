#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 15:25:26 2020

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

datadir = os.path.expanduser('~/Dropbox/Baabi_GarfieldDeviceDataDownload/Cockpit_418thFlightTestSquadron')

#%% Flight 1 Data ingestion

Sound = {'dev8': gf.Sounds(os.path.join(datadir, 'Device 8', 'FileNo1.txt'), ts='2019-06-10T16:10:00')['Sounds'],
         'devD': gf.Sounds(os.path.join(datadir, 'Device D','FileNoX.txt'), ts='2019-06-10T16:31:00')['Sounds']
         }


Motion = {'dev8': gf.Motion(os.path.join(datadir, 'Device 8', 'FileNo1.txt'), ts='2019-06-10T16:10:00')['Motion'],
          'devD': gf.Motion(os.path.join(datadir, 'Device D','FileNoX.txt'), ts='2019-06-10T16:31:00')['Motion']
          }


info = pd.read_excel(os.path.join(datadir,'FilesFrom418th.xlsx'), sheet_name = 'Flight 1')

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

    

#%% Making DFs
q1 = "Time < '2019-06-10 21:10:00' & Time > '2019-06-10 16:35:00'"
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

#%% Pre-takeoff to leveling off

plt.plot(sound_df['dev8']['2019-06-10 16:45:00':'2019-06-10 16:47:00'].rolling(512, center=True).mean())
plt.ylim(1018,1030)
ax = plt.gca()
ax.set_yticklabels([])
ax.set_yticks([])
plt.xticks(rotation=45)
plt.savefig('Cockpit/to1.png')
plt.clf()
plt.plot(sound_df['dev8']['2019-06-10 16:54:00':'2019-06-10 16:56:00'].rolling(512, center=True).mean())
plt.ylim(1018,1030)
ax = plt.gca()
ax.set_yticklabels([])
ax.set_yticks([])
plt.xticks(rotation=45)
plt.savefig('Cockpit/to2.png')
plt.clf()
plt.plot(sound_df['dev8']['2019-06-10 16:58:00':'2019-06-10 17:00:00'].rolling(512, center=True).mean())
plt.ylim(1018,1030)
ax = plt.gca()
ax.set_yticklabels([])
ax.set_yticks([])
plt.xticks(rotation=45)
plt.savefig('Cockpit/to3.png')
plt.clf()

plt.plot(sound_df['dev8']['2019-06-10 17:02:00':'2019-06-10 17:04:00'].rolling(512, center=True).mean())
plt.ylim(1018,1030)
plt.ylim(1018,1030)
ax = plt.gca()
ax.set_yticklabels([])
ax.set_yticks([])
plt.xticks(rotation=45)
plt.savefig('Cockpit/to4.png')
plt.clf()
#%% Tactical descent 1

d_landing_s = sound_df_smooth['2019-06-10 17:40':'2019-06-10 17:50']
d_landing_m = {}
for k in motion_df.keys():
    d_landing_m[k] = pd.DataFrame(motion_df[k])['2019-06-10 17:40':'2019-06-10 17:50']
    
interesting_times = ['17:46', '17:48']
interesting_dt = ['2019-06-10 ' + t for t in interesting_times]

plot_panel(d_landing_s, d_landing_m, 'devD', interesting_dt)
plt.savefig('Cockpit/tactical_landing_1.png')

d1 = d_landing_m['y']['2019-06-10 17:40':'2019-06-10 17:50']
plt.plot(d1['devD'])
plot_times([np.datetime64(u) for u in interesting_dt])
plot_panel(d_landing_s, d_landing_m, 'dev8', interesting_dt)

f, ax = plt.subplots(2,1, sharex=True)
d_landing_m['x'].plot(y = 'devD', ax = ax[0], legend=None, xlim = ['2019-06-10 17:45:00','2019-06-10 17:49:00'])
ax[0].set_ylabel('Device D Motion (x)', ha  = 'right', rotation='horizontal' )
d_landing_m['y'].plot(y = 'dev8', ax = ax[1], legend=None, xlim = ['2019-06-10 17:45:00','2019-06-10 17:49:00'])
ax[1].set_ylabel('Device 8 Motion (y)', ha  = 'right', rotation='horizontal' )
for i in range(len(ax)):
    ax[i].set_yticklabels([])
    ax[i].set_yticks([])
plt.savefig('Cockpit/orientation1.png')

plt.plot(d_landing_m['x']['devD'], ax= ax[0])
plt.plot(d_landing_m['y']['dev8'], ax = ax[1])


#%% Banks and rolls 1
d_landing_s = sound_df_smooth['2019-06-10 17:00':'2019-06-10 17:40']
d_landing_m = {}
for k in motion_df.keys():
    d_landing_m[k] = pd.DataFrame(motion_df_smooth[k])['2019-06-10 17:00':'2019-06-10 17:40']

interesting_dt = ['2019-06-10 ' + u  for u in ['17:07','17:12','17:35']]

plot_panel(d_landing_s, d_landing_m, 'dev8',interesting_dt)



#%% Tactical descent 2 and landing

d_landing_s = sound_df_smooth['2019-06-10 18:20':'2019-06-10 18:35']
d_landing_m = {}
for k in motion_df.keys():
    d_landing_m[k] = pd.DataFrame(motion_df[k])['2019-06-10 18:20':'2019-06-10 18:35']

interesting_times = ['18:21', '18:24','18:26', '18:33']
interesting_dt = ['2019-06-10 ' + u for u in interesting_times]


plot_panel(d_landing_s, d_landing_m,  'devD', interesting_dt)
plt.savefig('Cockpit/tactical_landing_2.png')
#%% Second sortie, touch and goes

d_tg2_s = sound_df_smooth['2019-06-10 19:50':'2019-06-10 20:40']
d_tg2_m = {}
d_tg2_m_smooth = {}
for k in motion_df.keys():
    d_tg2_m[k] = pd.DataFrame(motion_df[k])['2019-06-10 19:50':'2019-06-10 20:40']
    d_tg2_m_smooth[k] = d_tg2_m[k].rolling(10, center=True).mean()

    
tg_times = ['2019-06-10 19:57','2019-06-10 20:06', '2019-06-10 20:16','2019-06-10 20:25',
            '2019-06-10 20:28', '2019-06-10 20:33']

d_tg2_m_smooth['x'].plot(y='dev8')
for t in tg_times:
    plt.axvline(x=t, color ='g', linestyle='--')
    
    
    
    
    
    
    