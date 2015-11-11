#! /usr/bin/python

import os
import matplotlib as mpl

mpl.use('agg')

import matplotlib.pyplot as plt


plt.rc('text', usetex = True)
plt.rc('font', family = 'serif')

# StochasticSearch Data
ss_path       = "jl/"
ss_data       = []
ss_sample_run = [[], []]

# OpenTuner Data
ot_path       = "py/"
ot_data       = []
ot_sample_run = [[], []]

for run in os.listdir(ss_path):
    with open(ss_path + run + "/last.txt") as file:
        last = float(file.read().rstrip("\n").split(" ")[1])
        ss_data.append(last)

with open(ss_path + "run_2/best.txt") as file:
    text_points = file.read().splitlines()
    for line in text_points:
        point = line.split(" ")
        ss_sample_run[0].append(float(point[0]))
        ss_sample_run[1].append(float(point[1]))

for run in os.listdir(ot_path):
    with open(ot_path + run + "/best.txt") as file:
        best = file.read().splitlines()
        ot_data.append(float(best[-1].split(" ")[1]))

with open(ot_path + "run_2/best.txt") as file:
    text_points = file.read().splitlines()
    for line in text_points:
        point = line.split(" ")
        ot_sample_run[0].append(float(point[0]))
        ot_sample_run[1].append(float(point[1]))

boxplot_data = [ss_data, ot_data]

fig = plt.figure(1, figsize=(9, 6))

ax = fig.add_subplot(111)

bp = ax.boxplot(boxplot_data)

plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='darkgray')
plt.setp(bp['fliers'], color='red', marker='+')

ax.set_xticklabels(["StochasticSearch.jl", "OpenTuner"])

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)

ax.set_title("TSP Solution (532 Cities) Cost After Tuning for 10 minutes (6 runs)")
ax.set_xlabel("Tuner")
ax.set_ylabel("Solution Cost")

fig.savefig('att532_10min_comparison.eps', format = 'eps', dpi = 1000)

plt.clf()

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)

ax.set_xlim([-4, max(ss_sample_run[0]) + 4])

ax.scatter(ss_sample_run[0], ss_sample_run[1])
ax.plot(ss_sample_run[0], ss_sample_run[1])

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)

ax.set_title("Best TSP Solution (532 Cities) during a Tuning Run (StochasticSearch.jl)")
ax.set_xlabel("Tuning Time")
ax.set_ylabel("Solution Cost")

fig.savefig('att532_10min_best_ss.eps', format = 'eps', dpi = 1000)

plt.clf()

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)

ax.set_xlim([-4, max(ot_sample_run[0]) + 4])

ax.scatter(ot_sample_run[0], ot_sample_run[1])
ax.plot(ot_sample_run[0], ot_sample_run[1])

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)

ax.set_title("Best TSP Solution (532 Cities) during a Tuning Run (OpenTuner)")
ax.set_xlabel("Tuning Time")
ax.set_ylabel("Solution Cost")

fig.savefig('att532_10min_best_ot.eps', format = 'eps', dpi = 1000)
