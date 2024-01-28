# AUTHOR: BRIAN SMITH
# CREATED: 25/01/2023

import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import pandas as pd
import numpy as np

# sns.set_theme(style="darkgrid")
sns.set_style("ticks")

# read in pickled altitude data
altData = pd.read_pickle('altData.pkl')
altData = pd.melt(altData, 'date', ['meanAltitude', 'apogee', 'perigee'], 'Metric Type') # convert to wide format data frame

# Line plot of altitude data vs time
print('Plotting line plot')
fig = plt.figure(figsize=(14,7))
ax = sns.lineplot(data=altData, x='date', y='value', hue='Metric Type', errorbar=None)
sns.despine(offset=5, trim=True)

plt.title('International Space Station (ISS) - Mean Altitude, Apogee and Perigee vs. Time [2023]')
plt.xlabel('Time (date)')
plt.ylabel('Altitude Data (km)')
plt.legend()
plt.show()

print('Saving line plot.')
fig.savefig('ISS-AltitudeLinePlot2023.png')


# marker lines for crew dock/undock
print('Plotting line plot')
fig = plt.figure(figsize=(18,9))
ax = sns.lineplot(data=altData, x='date', y='value', hue='Metric Type', errorbar=None)
sns.despine(offset=5, trim=True)

plt.title('International Space Station (ISS) - Mean Altitude, Apogee and Perigee vs. Time [2023]')
plt.xlabel('Time (date)')
plt.ylabel('Altitude Data (km)')
plt.legend()

dates = [datetime(2023, 3, 2), datetime(2023, 3, 11), datetime(2023, 5, 22), datetime(2023, 5, 30),
         datetime(2023, 8, 27), datetime(2023, 9, 3), datetime(2023, 9, 15), datetime(2023, 9, 27)]
events = ['SpaceX Crew-6 Dock\n2023-03-02', 'SpaceX Crew-5 Undock\n2023-03-11', 'Axiom 2 Dock\n2023-05-22', 'Axiom 2 Undock\n2023-05-30',
          'SpaceX Crew-7 Dock\n2023-08-27', 'SpaceX Crew-6 Undock\n2023-09-03', 'Soyuz MS-24 Dock\n2023-09-15', 'Soyuz MS-23 Undock\n2023-09-27']
ymax = [424.5, 411, 423, 423, 422, 410, 424, 411]
ymin = [413, 423.5, 412, 412, 412, 420, 414, 422]
align = ['l', 'r', 'l', 'r', 'l', 'l', 'r', 'r']

plt.vlines(x=dates, ymin=ymin, ymax=ymax, colors='black', lw=1.5, ls=['-', '--', '-', '--', '-', '--', '-', '--'])

# annotate lines
for d, e, l, a  in zip(dates, events, ymax, align):
    ax.annotate(e, xy=(d, l),
                xytext=(-3, 0) if a=='l' else (3, 0), textcoords="offset points",
                horizontalalignment="right" if a=='l' else "left",
                verticalalignment="bottom" if l < 415 else "top")

plt.show()

print('Saving line plot.')
fig.savefig('ISS-AltitudeLinePlotAnnotated2023.png')