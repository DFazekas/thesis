#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function

from optparse import OptionParser
import os
import sys

# We need to import some python modules from the $SUMO_HOME/tools directory.
if 'SUMO_HOME' in os.environ:
    print('Found "SUMO_HOME" in os environment vars')
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    print(tools)
    sys.path.append(tools)
else:
    sys.exit('please declare environment variable: "SUMO_HOME"')


# Checks for the binary in environment variables.
# from sumolib import checkBinary
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()


# print(plot_trajectories)
# print(sys.path)


# # Time vs Distance plot
# sys.argv[1:] = ['report_fcd.xml', '-t', 'td', '-o', 'plots/plot_td.png']
# plot_trajectories.main(plot_trajectories.getOptions())

# # Time vs Speed plot
# sys.argv[1:] = ['report_fcd.xml', '-t', 'ts', '-o', 'plots/plot_ts.png']
# plot_trajectories.main(plot_trajectories.getOptions())

# # Time vs Acceleration plot
# sys.argv[1:] = ['report_fcd.xml', '-t', 'ta', '-o', 'plots/plot_ta.png']
# plot_trajectories.main(plot_trajectories.getOptions())

# # Distance vs Speed plot
# sys.argv[1:] = ['report_fcd.xml', '-t', 'ds', '-o', 'plots/plot_ds.png']
# plot_trajectories.main(plot_trajectories.getOptions())

# # Distance vs Acceleration plot
# sys.argv[1:] = ['report_fcd.xml', '-t', 'da', '-o', 'plots/plot_da.png']
# plot_trajectories.main(plot_trajectories.getOptions())
