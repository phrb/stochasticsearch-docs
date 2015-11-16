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

# StochasticSearch Data
ss_path       = "jl/30min/"
ss_data       = []
ss_sample_run = [[], []]

# OpenTuner Data
ot_path       = "py/30min/"
ot_data       = []
ot_sample_run = [[], []]

# Optimal
opt = "optimal.txt"

with open(ss_path + "run_1/best.txt") as file:
    text_points = file.read().splitlines()
    for line in text_points:
        point = line.split(" ")
        ss_sample_run[0].append(float(point[0]))
        ss_sample_run[1].append(float(point[1]))

with open(ot_path + "run_1/best.txt") as file:
    text_points = file.read().splitlines()
    for line in text_points:
        point = line.split(" ")
        ot_sample_run[0].append(float(point[0]))
        ot_sample_run[1].append(float(point[1]))

with open(opt) as file:
    opt_line = float(file.read().rstrip("\n"))

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)

ax.set_xlim([-4, max(max(ss_sample_run[0]), max(ot_sample_run[0])) + 4])

ax.set_ylim([opt_line - 5000, max(max(ss_sample_run[1]), max(ot_sample_run[1])) + 5000])

ss_b = ax.scatter(ss_sample_run[0], ss_sample_run[1], marker = 'x', color = 'c')
ax.plot(ss_sample_run[0], ss_sample_run[1], color = 'c')

ot_b = ax.scatter(ot_sample_run[0], ot_sample_run[1], marker = 'o', color = 'g')
ax.plot(ot_sample_run[0], ot_sample_run[1], color = 'g')

plt.hlines(opt_line, -4, max(ss_sample_run[0]) + 4, linestyles='dashed')

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.5)

ax.set_title("Best TSP Solution (48 Cities) during a Tuning Run")
ax.set_xlabel("Tuning Time")
ax.set_ylabel("Solution Cost")

plt.legend((ss_b, ot_b),
           ('StochasticSearch.jl', 'OpenTuner'),
           prop = {'size' : 14})

fig.savefig('att48_30min_best_comparison.eps', format = 'eps', dpi = 1000)
