#!/usr/bin/python
"""
Plotting script for Main Figure 4A
"""
__author__ = 'cfortes-lima'

# Run Beagle's phasing and estimate Ne with IBDNe.
# IBDNe results for the last 300 generationss with 95%CI
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import argparse
import pandas as pd
import random, pdb
import numpy as np

# Bokeh imports
from bokeh.io.export import export_svgs, export_png
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import column
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Label, Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', default='01-Main_Figures/Figure_4A')
args = parser.parse_args()

# Usage
#
# python3 scripts/bokeh_Figure_4A.py --output "01-Main_Figures/Figure_4A"

# Data
title='Figure 4A | Effective population sizes (Ne) estimated for each Fulani population.'

generations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

# IBDNe results for each Fulani population:
Senegal_Fulani_Linguere = [6.79E+04, 5.28E+04, 4.05E+04, 3.06E+04, 2.25E+04, 1.59E+04, 1.06E+04, 6.49E+03, 4.87E+03, 4.06E+03, 3.61E+03, 3.36E+03, 3.24E+03, 3.23E+03, 3.35E+03, 3.62E+03, 3.92E+03, 4.24E+03, 4.60E+03, 5.01E+03, 5.50E+03, 6.12E+03, 6.94E+03, 8.04E+03, 9.47E+03, 1.14E+04, 1.39E+04, 1.75E+04, 2.25E+04, 2.97E+04, 3.97E+04, 5.36E+04, 7.38E+04, 1.04E+05, 1.50E+05, 2.21E+05, 3.32E+05, 5.02E+05, 7.60E+05, 1.14E+06, 1.77E+06, 2.80E+06, 4.53E+06, 7.43E+06, 1.23E+07, 2.02E+07, 3.33E+07, 5.47E+07, 9.22E+07, 1.59E+08, 2.77E+08]
Gambia_Fula = [8.05E+10, 2.39E+09, 5.67E+07, 3.66E+05, 2.19E+05, 1.20E+06, 1.04E+07, 6.94E+07, 3.12E+08, 9.76E+08, 2.20E+09, 3.62E+09, 4.00E+09, 2.41E+09, 7.81E+08, 1.77E+08, 3.61E+07, 7.90E+06, 1.90E+06, 5.17E+05, 1.65E+05, 6.31E+04, 2.86E+04, 1.56E+04, 9.74E+03, 6.88E+03, 5.49E+03, 4.94E+03, 5.00E+03, 5.62E+03, 6.97E+03, 9.61E+03, 1.43E+04, 2.31E+04, 4.04E+04, 7.59E+04, 1.52E+05, 3.21E+05, 7.19E+05, 1.67E+06, 4.17E+06, 1.12E+07, 3.18E+07, 9.48E+07, 2.92E+08, 9.27E+08, 3.02E+09, 1.00E+10, 3.51E+10, 1.30E+11, 4.99E+11]
Senegal_Halpularen = [3.25E+04, 3.15E+04, 3.02E+04, 2.83E+04, 2.58E+04, 2.27E+04, 1.89E+04, 1.49E+04, 1.42E+04, 1.51E+04, 1.73E+04, 2.06E+04, 2.53E+04, 3.18E+04, 4.05E+04, 5.23E+04, 6.62E+04, 8.19E+04, 9.87E+04, 1.16E+05, 1.32E+05, 1.47E+05, 1.60E+05, 1.71E+05, 1.80E+05, 1.88E+05, 1.96E+05, 2.02E+05, 2.08E+05, 2.14E+05, 2.20E+05, 2.25E+05, 2.32E+05, 2.41E+05, 2.51E+05, 2.63E+05, 2.78E+05, 2.95E+05, 3.15E+05, 3.39E+05, 3.68E+05, 4.03E+05, 4.45E+05, 4.95E+05, 5.55E+05, 6.26E+05, 7.12E+05, 8.15E+05, 9.41E+05, 1.10E+06, 1.28E+06]
Mauritania_Fulani_Assaba = [1.65E+16, 3.42E+15, 7.00E+14, 1.42E+14, 2.80E+13, 5.27E+12, 8.38E+11, 5.33E+10, 5.73E+09, 8.55E+08, 1.65E+08, 3.94E+07, 1.13E+07, 3.84E+06, 1.49E+06, 6.63E+05, 3.28E+05, 1.78E+05, 1.05E+05, 6.72E+04, 4.58E+04, 3.32E+04, 2.55E+04, 2.05E+04, 1.73E+04, 1.53E+04, 1.40E+04, 1.33E+04, 1.31E+04, 1.32E+04, 1.38E+04, 1.48E+04, 1.62E+04, 1.82E+04, 2.09E+04, 2.46E+04, 2.94E+04, 3.58E+04, 4.43E+04, 5.58E+04, 7.13E+04, 9.24E+04, 1.21E+05, 1.62E+05, 2.18E+05, 2.97E+05, 4.10E+05, 5.71E+05, 8.03E+05, 1.14E+06, 1.63E+06]
Guinea_Fulani = [5.49E+04, 5.04E+04, 4.60E+04, 4.16E+04, 3.73E+04, 3.31E+04, 2.90E+04, 2.51E+04, 2.37E+04, 2.35E+04, 2.41E+04, 2.55E+04, 2.77E+04, 3.08E+04, 3.52E+04, 4.17E+04, 4.94E+04, 5.88E+04, 7.05E+04, 8.54E+04, 1.05E+05, 1.30E+05, 1.64E+05, 2.09E+05, 2.71E+05, 3.56E+05, 4.72E+05, 6.36E+05, 8.67E+05, 1.20E+06, 1.67E+06, 2.34E+06, 3.32E+06, 4.76E+06, 6.89E+06, 1.01E+07, 1.48E+07, 2.18E+07, 3.23E+07, 4.79E+07, 7.16E+07, 1.08E+08, 1.63E+08, 2.46E+08, 3.74E+08, 5.68E+08, 8.63E+08, 1.31E+09, 2.00E+09, 3.06E+09, 4.68E+09]
Mali_Fulani_InnerDelta = [2.72E+04, 2.99E+04, 3.25E+04, 3.52E+04, 3.79E+04, 4.05E+04, 4.31E+04, 4.57E+04, 4.65E+04, 4.56E+04, 4.28E+04, 3.84E+04, 3.31E+04, 2.75E+04, 2.21E+04, 1.75E+04, 1.39E+04, 1.13E+04, 9.30E+03, 7.83E+03, 6.75E+03, 5.98E+03, 5.47E+03, 5.24E+03, 5.13E+03, 5.15E+03, 5.31E+03, 5.62E+03, 6.10E+03, 6.83E+03, 7.89E+03, 9.42E+03, 1.14E+04, 1.42E+04, 1.79E+04, 2.30E+04, 3.03E+04, 4.06E+04, 5.53E+04, 7.60E+04, 1.06E+05, 1.50E+05, 2.15E+05, 3.14E+05, 4.63E+05, 6.89E+05, 1.03E+06, 1.54E+06, 2.33E+06, 3.58E+06, 5.55E+06]
Mali_Fulani_Diafarabe = [9.31E+06, 6.46E+06, 4.46E+06, 3.04E+06, 2.04E+06, 1.33E+06, 8.01E+05, 4.10E+05, 2.56E+05, 1.77E+05, 1.30E+05, 9.84E+04, 7.58E+04, 5.92E+04, 4.67E+04, 3.74E+04, 2.99E+04, 2.39E+04, 1.92E+04, 1.56E+04, 1.29E+04, 1.09E+04, 9.32E+03, 8.18E+03, 7.37E+03, 6.83E+03, 6.51E+03, 6.38E+03, 6.43E+03, 6.65E+03, 7.06E+03, 7.68E+03, 8.59E+03, 9.86E+03, 1.16E+04, 1.40E+04, 1.72E+04, 2.17E+04, 2.79E+04, 3.65E+04, 4.88E+04, 6.65E+04, 9.21E+04, 1.30E+05, 1.85E+05, 2.69E+05, 3.98E+05, 5.96E+05, 9.06E+05, 1.39E+06, 2.16E+06]
BurkinaFaso_Fulani_Banfora = [1.77E+03, 3.64E+03, 7.06E+03, 9.92E+03, 2.13E+04, 4.36E+04, 8.06E+04, 1.42E+05, 2.34E+05, 3.55E+05, 4.87E+05, 5.51E+05, 4.98E+05, 3.76E+05, 2.54E+05, 1.61E+05, 9.61E+04, 5.68E+04, 3.36E+04, 2.08E+04, 1.34E+04, 9.07E+03, 6.41E+03, 4.85E+03, 3.85E+03, 3.16E+03, 2.90E+03, 2.74E+03, 2.68E+03, 2.73E+03, 2.92E+03, 3.32E+03, 3.90E+03, 4.73E+03, 6.01E+03, 7.79E+03, 1.03E+04, 1.41E+04, 1.98E+04, 2.85E+04, 4.17E+04, 6.23E+04, 9.28E+04, 1.42E+05, 2.22E+05, 3.55E+05, 5.73E+05, 9.28E+05, 1.52E+06, 2.51E+06, 4.15E+06]
BurkinaFaso_Fulani_Ziniare = [1.20E+04, 1.27E+04, 1.32E+04, 1.37E+04, 1.40E+04, 1.42E+04, 1.43E+04, 1.42E+04, 1.36E+04, 1.25E+04, 1.09E+04, 9.14E+03, 7.31E+03, 5.63E+03, 4.22E+03, 3.10E+03, 2.35E+03, 1.85E+03, 1.51E+03, 1.28E+03, 1.12E+03, 1.02E+03, 9.84E+02, 1.05E+03, 1.15E+03, 1.29E+03, 1.49E+03, 1.77E+03, 2.19E+03, 2.80E+03, 3.72E+03, 5.09E+03, 7.07E+03, 9.98E+03, 1.44E+04, 2.13E+04, 3.23E+04, 4.99E+04, 7.76E+04, 1.20E+05, 1.88E+05, 3.00E+05, 4.91E+05, 8.21E+05, 1.39E+06, 2.37E+06, 4.04E+06, 6.85E+06, 1.17E+07, 2.04E+07, 3.62E+07]
BurkinaFaso_Fulani_Tindangou = [1.88E+06, 1.28E+06, 8.67E+05, 5.84E+05, 3.91E+05, 2.58E+05, 1.68E+05, 1.07E+05, 7.48E+04, 5.28E+04, 3.73E+04, 2.64E+04, 1.88E+04, 1.34E+04, 9.71E+03, 7.14E+03, 5.23E+03, 3.93E+03, 3.06E+03, 2.47E+03, 2.08E+03, 1.81E+03, 1.63E+03, 1.53E+03, 1.54E+03, 1.61E+03, 1.74E+03, 1.93E+03, 2.21E+03, 2.61E+03, 3.17E+03, 3.98E+03, 5.17E+03, 6.87E+03, 9.31E+03, 1.29E+04, 1.82E+04, 2.64E+04, 3.91E+04, 5.88E+04, 8.91E+04, 1.36E+05, 2.12E+05, 3.37E+05, 5.44E+05, 8.96E+05, 1.50E+06, 2.52E+06, 4.24E+06, 7.18E+06, 1.23E+07]
Niger_Fulani_Ader = [3.38E+04, 4.60E+04, 6.14E+04, 8.05E+04, 1.03E+05, 1.30E+05, 1.60E+05, 1.94E+05, 2.20E+05, 2.35E+05, 2.33E+05, 2.13E+05, 1.75E+05, 1.30E+05, 8.82E+04, 5.66E+04, 3.55E+04, 2.23E+04, 1.44E+04, 9.69E+03, 6.81E+03, 5.01E+03, 3.87E+03, 3.15E+03, 2.71E+03, 2.45E+03, 2.33E+03, 2.31E+03, 2.38E+03, 2.55E+03, 2.85E+03, 3.32E+03, 4.01E+03, 5.02E+03, 6.47E+03, 8.58E+03, 1.17E+04, 1.64E+04, 2.37E+04, 3.50E+04, 5.27E+04, 8.11E+04, 1.27E+05, 2.03E+05, 3.31E+05, 5.51E+05, 9.35E+05, 1.61E+06, 2.79E+06, 4.89E+06, 8.68E+06]
Niger_Fulani_Abalak = [2.05E+05, 1.53E+05, 1.13E+05, 8.35E+04, 6.13E+04, 4.47E+04, 3.24E+04, 2.33E+04, 1.76E+04, 1.36E+04, 1.06E+04, 8.39E+03, 6.69E+03, 5.41E+03, 4.43E+03, 3.69E+03, 3.10E+03, 2.65E+03, 2.31E+03, 2.07E+03, 1.90E+03, 1.79E+03, 1.73E+03, 1.72E+03, 1.78E+03, 1.88E+03, 2.04E+03, 2.26E+03, 2.57E+03, 2.97E+03, 3.52E+03, 4.25E+03, 5.26E+03, 6.62E+03, 8.47E+03, 1.10E+04, 1.46E+04, 1.96E+04, 2.67E+04, 3.68E+04, 5.13E+04, 7.23E+04, 1.03E+05, 1.49E+05, 2.19E+05, 3.24E+05, 4.84E+05, 7.29E+05, 1.10E+06, 1.67E+06, 2.57E+06]
Niger_Fulani_Zinder = [3.35E+04, 3.86E+04, 4.39E+04, 4.93E+04, 5.49E+04, 6.05E+04, 6.60E+04, 7.13E+04, 7.42E+04, 7.45E+04, 7.23E+04, 6.79E+04, 6.22E+04, 5.59E+04, 4.97E+04, 4.42E+04, 4.01E+04, 3.72E+04, 3.54E+04, 3.46E+04, 3.46E+04, 3.55E+04, 3.70E+04, 3.89E+04, 4.16E+04, 4.53E+04, 5.01E+04, 5.61E+04, 6.38E+04, 7.34E+04, 8.51E+04, 9.93E+04, 1.17E+05, 1.39E+05, 1.66E+05, 2.00E+05, 2.42E+05, 2.95E+05, 3.61E+05, 4.45E+05, 5.50E+05, 6.83E+05, 8.52E+05, 1.07E+06, 1.33E+06, 1.68E+06, 2.11E+06, 2.67E+06, 3.39E+06, 4.31E+06, 5.49E+06]
Niger_Fulani_Diffa = [3.33E+07, 1.85E+07, 1.01E+07, 5.36E+06, 2.74E+06, 1.29E+06, 5.05E+05, 1.29E+05, 5.56E+04, 3.06E+04, 1.97E+04, 1.41E+04, 1.11E+04, 9.51E+03, 8.93E+03, 9.41E+03, 1.03E+04, 1.16E+04, 1.34E+04, 1.59E+04, 1.92E+04, 2.36E+04, 2.96E+04, 3.74E+04, 4.76E+04, 6.11E+04, 7.88E+04, 1.02E+05, 1.33E+05, 1.73E+05, 2.25E+05, 2.94E+05, 3.83E+05, 5.01E+05, 6.55E+05, 8.57E+05, 1.12E+06, 1.46E+06, 1.91E+06, 2.50E+06, 3.27E+06, 4.27E+06, 5.59E+06, 7.31E+06, 9.56E+06, 1.25E+07, 1.64E+07, 2.14E+07, 2.80E+07, 3.67E+07, 4.82E+07]
Niger_Fulani_Balatungur = [9.44E+04, 7.92E+04, 6.65E+04, 5.57E+04, 4.67E+04, 3.91E+04, 3.27E+04, 2.73E+04, 2.30E+04, 1.91E+04, 1.58E+04, 1.29E+04, 1.05E+04, 8.57E+03, 6.98E+03, 5.71E+03, 4.71E+03, 3.97E+03, 3.42E+03, 3.02E+03, 2.74E+03, 2.56E+03, 2.46E+03, 2.44E+03, 2.50E+03, 2.62E+03, 2.80E+03, 3.06E+03, 3.41E+03, 3.89E+03, 4.53E+03, 5.40E+03, 6.54E+03, 8.06E+03, 1.01E+04, 1.28E+04, 1.65E+04, 2.15E+04, 2.85E+04, 3.81E+04, 5.16E+04, 7.05E+04, 9.76E+04, 1.37E+05, 1.94E+05, 2.77E+05, 3.99E+05, 5.77E+05, 8.39E+05, 1.23E+06, 1.83E+06]
Cameroon_Fulani_Tcheboua = [1.55E+04, 2.24E+04, 3.20E+04, 1.17E+04, 2.35E+04, 7.75E+04, 1.25E+05, 1.77E+05, 2.44E+05, 3.35E+05, 4.57E+05, 6.15E+05, 6.84E+05, 4.71E+05, 1.95E+05, 6.10E+04, 2.24E+04, 9.58E+03, 4.75E+03, 2.81E+03, 1.82E+03, 1.28E+03, 9.75E+02, 8.80E+02, 8.73E+02, 9.49E+02, 1.13E+03, 1.49E+03, 2.04E+03, 3.00E+03, 4.80E+03, 8.18E+03, 1.46E+04, 2.73E+04, 5.21E+04, 9.92E+04, 2.07E+05, 4.62E+05, 1.07E+06, 2.47E+06, 5.71E+06, 1.32E+07, 3.01E+07, 6.80E+07, 1.73E+08, 4.58E+08, 1.22E+09, 3.23E+09, 8.63E+09, 2.31E+10, 6.18E+10]
Chad_Fulani_Linia = [2.52E+04, 3.25E+04, 4.11E+04, 5.08E+04, 6.08E+04, 6.97E+04, 7.52E+04, 7.57E+04, 1.35E+05, 1.78E+05, 2.01E+05, 2.06E+05, 1.93E+05, 1.64E+05, 1.30E+05, 9.68E+04, 7.20E+04, 5.28E+04, 3.89E+04, 2.92E+04, 2.24E+04, 1.76E+04, 1.39E+04, 1.08E+04, 9.14E+03, 7.99E+03, 7.19E+03, 6.62E+03, 6.22E+03, 5.94E+03, 5.78E+03, 5.70E+03, 6.60E+03, 7.54E+03, 8.59E+03, 9.82E+03, 1.13E+04, 1.31E+04, 1.55E+04, 1.86E+04, 2.22E+04, 2.70E+04, 3.31E+04, 4.11E+04, 5.16E+04, 6.56E+04, 8.44E+04, 1.10E+05, 1.43E+05, 1.87E+05, 2.47E+05]
Chad_Fulani_Bongor = [6.05E+04, 8.21E+04, 1.08E+05, 1.37E+05, 1.64E+05, 1.80E+05, 1.74E+05, 1.44E+05, 2.19E+05, 3.54E+05, 4.96E+05, 6.02E+05, 6.21E+05, 5.29E+05, 3.72E+05, 2.28E+05, 1.38E+05, 8.23E+04, 4.85E+04, 2.92E+04, 1.83E+04, 1.20E+04, 8.13E+03, 5.38E+03, 3.78E+03, 3.13E+03, 2.73E+03, 2.51E+03, 2.42E+03, 2.43E+03, 2.51E+03, 2.69E+03, 3.24E+03, 4.20E+03, 5.47E+03, 7.22E+03, 9.74E+03, 1.34E+04, 1.91E+04, 2.81E+04, 4.14E+04, 6.08E+04, 9.14E+04, 1.40E+05, 2.18E+05, 3.49E+05, 5.72E+05, 9.68E+05, 1.64E+06, 2.77E+06, 4.73E+06]

leg_1 = []
pop_name = ['Mauritania_Fulani_Assaba','Senegal_Fulani_Linguere','Senegal_Halpularen','Gambia_Fula','Guinea_Fulani','Mali_Fulani_Diafarabe','Mali_Fulani_InnerDelta','BurkinaFaso_Fulani_Banfora','BurkinaFaso_Fulani_Tindangou','BurkinaFaso_Fulani_Ziniare','Niger_Fulani_Abalak','Niger_Fulani_Ader','Niger_Fulani_Balatungur','Niger_Fulani_Diffa','Niger_Fulani_Zinder','Cameroon_Fulani_Tcheboua','Chad_Fulani_Bongor','Chad_Fulani_Linia']
pop_data= ([Mauritania_Fulani_Assaba,Senegal_Fulani_Linguere,Senegal_Halpularen,Gambia_Fula,Guinea_Fulani,Mali_Fulani_Diafarabe,Mali_Fulani_InnerDelta,BurkinaFaso_Fulani_Banfora,BurkinaFaso_Fulani_Tindangou,BurkinaFaso_Fulani_Ziniare,Niger_Fulani_Abalak,Niger_Fulani_Ader,Niger_Fulani_Balatungur,Niger_Fulani_Diffa,Niger_Fulani_Zinder,Cameroon_Fulani_Tcheboua,Chad_Fulani_Bongor,Chad_Fulani_Linia])

# Plotting pattern
colours= ['#66AEBF','#3B9AB2','#57A7BA','#49A0B6','#74B5C3','#8CBAA9','#C2C460','#A7BF85','#E9C825','#DDC93C','#E5BA11','#E7C11B','#E58300','#E2A600','#E2B407','#E58300','#F21A00','#EE3D00','#004529','#ADDD8E','#78C679','#238443','#41AB5D','#ADDD8E','#238443','#006837','#004529','#004529','#ADDD8E','#006837','#78C679','#78C679','#41AB5D','#ADDD8E','#238443','#006837','#41AB5D','#543005','#8C510A','#BF812D','#DFC27D','#543005','#8C510A','#BF812D','#DFC27D','#543005','#BF812D','#DFC27D','#543005','#DFC27D','#8C510A','tan','tan','tan','tan','skyblue','skyblue','skyblue','skyblue','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray']
markers= ['x','circle','cross','triangle','diamond','inverted_triangle','asterisk','square_x','circle_cross','diamond_cross','circle_x','square_cross','triangle','square','square','circle','circle','diamond','square_cross','triangle','cross','x','diamond','inverted_triangle','square','circle_x','square_cross','diamond_cross','asterisk','square','circle_cross','circle','triangle','diamond','cross','circle','triangle','asterisk','x','square_x','diamond','inverted_triangle','circle_cross','square_cross','circle_x','diamond_cross','square','triangle','square','circle','diamond','circle','triangle','cross','x','diamond','inverted_triangle','square_x','asterisk','circle','square_cross','circle_cross','circle_x','diamond_cross','square','square']
filling= [None,None,None,None,None,None,None,None,None,None,None,None,'#E58300','#E2A600',None,'#E58300',None,'#EE3D00',None,None,None,None,None,None,'#238443',None,None,None,None,None,None,'#78C679',None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,'#8C510A','#DFC27D','#8C510A','#543005',None,None,None,None,None,None,None,None,'#737373',None,None,None,None,'#737373',None]

# Plot the last 50 generations
plot = figure(title=title, x_range=[4, 50], y_range=[1E2, 1E18], toolbar_location="above", width = 1400, height = 800,
	x_axis_label="Generations", y_axis_label="Effective population size, log10(Ne)", y_axis_type="log", tools='pan,box_zoom,xwheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='xwheel_zoom')

for counter,pop in enumerate(pop_name):
	leg_1.append((pop, [plot.line(name=pop, x=generations, y=pop_data[counter], muted_alpha=0.2, line_width=5, line_color=colours[counter]) ] )) # , line_dash=line_dash[counter]

plot.title.text_font_size= '21pt'
label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption= Label(text=' Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).', **label_opts)
plot.add_layout(caption, "above")

#plot.xaxis.axis_label=""
plot.xaxis.axis_label_text_font_size= "20pt"
plot.xaxis.major_label_text_font_size= "19pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 4

#plot.yaxis.axis_label=""
plot.yaxis.axis_label_text_font_size= "20pt"
plot.yaxis.major_label_text_font_size= "18pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 4

#Grid lines
plot.xgrid.visible = False
plot.ygrid.visible = False

legend1 = Legend(
    items=leg_1[0:], location=(0, -30))

plot.add_layout(legend1, 'right')
plot.legend.location = "top_center"
plot.legend.click_policy="hide" #"mute"
plot.legend.label_text_font_size = '10pt'
plot.legend.label_text_font_style= "normal" # "bold" or "italic"

plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [
	 ('Population', '$name'),
		 ]
	 ))

# Show and Save plot in PNG format.
print('Plotting Figure 4A')
show(plot)

export_png(plot, filename=args.output+".png")

# plot.output_backend= "svg"
# export_svgs(plot, filename=args.output+".svg")

exit()

######################
