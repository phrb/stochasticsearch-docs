#! /usr/bin/python

import os
import matplotlib as mpl

mpl.use('agg')

import matplotlib.pyplot as plt

plt.rc('text', usetex = True)
plt.rc('font', family = 'serif')

font = {'family' : 'serif',
        'size'   : 18}

mpl.rc('font', **font)

# StochasticSearch Seq
ss_path           = "jl//15min/seq/"
ss_data           = []
ss_sample_run     = [[], []]

# StochasticSearch Par
ss_par_path       = "jl//15min/par/"
ss_par_data       = []
ss_par_sample_run = [[], []]

# OpenTuner Data
ot_path           = "py/15min/"
ot_data           = []
ot_sample_run     = [[], []]

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

for run in os.listdir(ss_par_path):
    with open(ss_par_path + run + "/last.txt") as file:
        last = float(file.read().rstrip("\n").split(" ")[1])
        ss_par_data.append(last)

with open(ss_par_path + "run_1/best.txt") as file:
    text_points = file.read().splitlines()
    for line in text_points:
        point = line.split(" ")
        ss_par_sample_run[0].append(float(point[0]))
        ss_par_sample_run[1].append(float(point[1]))

for run in os.listdir(ot_path):
    with open(ot_path + run + "/best.txt") as file:
        best = file.read().splitlines()
        ot_data.append(float(best[-1].split(" ")[1]))

with open(ot_path + "run_1/best.txt") as file:
    text_points = file.read().splitlines()
    for line in text_points:
        point = line.split(" ")
        ot_sample_run[0].append(float(point[0]))
        ot_sample_run[1].append(float(point[1]))

boxplot_data = [ss_data, ot_data, ss_par_data]

fig = plt.figure(1, figsize=(9, 6))

ax = fig.add_subplot(111)

bp = ax.boxplot(boxplot_data)

plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='darkgray')
plt.setp(bp['fliers'], color='red', marker='+')

ax.set_xticklabels(["StochasticSearch.jl (seq)", "OpenTuner", "StochasticSearch.jl (p = 4)"])

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)

ax.set_title("TSP Solution (85900 Cities) Cost After Tuning for 15 minutes (4 runs)")
ax.set_xlabel("Tuner")
ax.set_ylabel("Solution Cost")

fig.savefig('par_pla85900_15min_comparison.eps', format = 'eps', dpi = 1000)

plt.clf()

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)

ax.set_xlim([-10, max(max(ss_sample_run[0]), max(ot_sample_run[0]), max(ss_par_sample_run[0])) + 10])

#ax.set_ylim([min(min(ss_sample_run[1]), min(ot_sample_run[1]), min(ss_par_sample_run[1])) - 400000, max(max(ss_sample_run[1]), max(ot_sample_run[1]), max(ss_par_sample_run[1])) + 400000])

ax.set_ylim(141895033)

axhline(y=141895033.,color='b',ls='dashed')

ss_b = ax.scatter(ss_sample_run[0], ss_sample_run[1], marker = 'x', color = 'c')
ax.plot(ss_sample_run[0], ss_sample_run[1], color = 'c')

ot_b = ax.scatter(ot_sample_run[0], ot_sample_run[1], marker = 'o', color = 'g')
ax.plot(ot_sample_run[0], ot_sample_run[1], color = 'g')

ss_par_b = ax.scatter(ss_par_sample_run[0], ss_par_sample_run[1], marker = 'x', color = 'b')
ax.plot(ss_par_sample_run[0], ss_par_sample_run[1], color = 'b')

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)

ax.set_title("Best TSP Solution (85900 Cities) during a Tuning Run")
ax.set_xlabel("Tuning Time")
ax.set_ylabel("Solution Cost")

plt.legend((ss_b, ot_b, ss_par_b),
           ('StochasticSearch.jl (seq)', 'OpenTuner', 'StochasticSearch.jl (p = 4)'),
           prop = {'size' : 14})

fig.savefig('par_pla85900_15min_best_comparison.eps', format = 'eps', dpi = 1000)
