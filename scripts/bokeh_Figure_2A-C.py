"""
Plotting script for Main Figure 2A and 2C
"""
__author__ = 'Cesar Fortes-Lima'

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import numpy as np
import warnings
import sys, random, csv
warnings.filterwarnings('ignore')

#import pdb
from io import StringIO
from tabulate import tabulate

# Bokeh imports
from bokeh.io.export import export_svg, export_png
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, gridplot, layout
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Label, Legend, HoverTool, WheelZoomTool, ColumnDataSource, Span
from bokeh.transform import linear_cmap
from bokeh.models.layouts import TabPanel, Tabs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('--input_A', default='Tables/Fulani_aDNA-Modern_DB.evec') #assumes eval in same place
parser.add_argument('--input_B', default='Tables/Fulani_aDNA-Modern_DB.evec') #assumes eval in same place
parser.add_argument('--pattern_A', default='Tables/Fulani_aDNA-Modern_DB_pca.csv')
parser.add_argument('--pattern_B', default='Tables/Fulani_aDNA-Modern_DB_grey.csv')
parser.add_argument('-o', '--output', default='02-Suppl_Figures/Main_Figure_2C')
# Optional
parser.add_argument('--title', default='Main Figure 2C | PCA for modern populations')
parser.add_argument('--which_pcs', default='1,2')
args = parser.parse_args()

# Usage: 
# Table_A='Tables/Fulani-World_DB'
# Table_B='Tables/Fulani_aDNA-Modern_DB'
#
# python3 scripts/bokeh_Figure_2A-C.py --input_A ${Table_A}.pca.evec --input_B ${Table_B}.pca.evec \
# --pattern_A ${Table_A}_pca.csv --pattern_B ${Table_B}_grey.csv -o 01-Main_Figures/Figure_2A-C
#

####################

# PCA Plot 2A
title_b= "Figure 2A | PCA plot for modern populations"
which_pcs= (1,2)
print ('Plotting',['PC' + str(p) + ' ' for p in which_pcs])

# Read table
evec = open(args.input_A)
which_pcs = list(map(int, args.which_pcs.split(',')))

my_eval = open(args.input_A.replace('evec', 'eval'))
eval_per = []
for line in my_eval:
    eval_per.append(float(line.strip()))
eval_per = [x/sum(eval_per)*100 for x in eval_per]

eigs = {}
evec.readline()
evec_all = pd.read_csv(evec, header=None, sep=r'\s+') #, skiprows=1)
pcs = ['ID']
pcs.extend(['PC' + str(x) for x in range(1, evec_all.shape[1]-1)])
pcs.append('PC')
evec_all.columns = pcs
iid_fid = pd.DataFrame(evec_all['ID'].str.split(':').tolist())
df = pd.concat([iid_fid, evec_all], axis=1)
df.rename(columns={0: 'FID', 1: 'IID'}, inplace=True)
source = df
source.set_index('FID')
source  = source.rename(columns={0: "FID", 1: "IID"})
fids = source.FID.unique()

output_file(args.output+'.html', mode='inline')

# Set your own pattern
ifile  = open(args.pattern_A, 'r')
pattern = csv.reader(ifile)
sizes, labels, colours, markers, filling = [], [], [], [], []

for row in pattern:
	sizes.append(row[0])
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling = [d if d!='None' else None for d in filling]

sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

plot_a = figure(title=title_b, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width=1600, height= 800,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_a.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption= Label(text=' Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).', **label_opts)
plot_a.add_layout(caption, "above")
plot_a.title.text_font_size = '18pt'

#plot_a.xaxis.axis_label="PC1"
plot_a.xaxis.axis_label= "PC"+str(which_pcs[0])+' ('+"%.2f" % eval_per[which_pcs[0]-1]+'% var explained)'
plot_a.xaxis.axis_label_text_font_size = '16pt'
plot_a.xaxis.major_label_text_font_size = '15pt'
plot_a.xaxis.axis_label_text_font= "arial"
plot_a.xaxis.axis_label_text_color= "black"
plot_a.xaxis.major_label_text_color= "black"
plot_a.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_tick_line_width= 5

#plot_a.yaxis.axis_label="PC2"
plot_a.yaxis.axis_label= "PC"+str(which_pcs[1])+' ('+"%.2f" % eval_per[which_pcs[1]-1]+'% var explained)'
plot_a.yaxis.axis_label_text_font_size = '16pt'
plot_a.yaxis.major_label_text_font_size = '15pt'
plot_a.yaxis.axis_label_text_font= "arial"
plot_a.yaxis.axis_label_text_color= "black"
plot_a.yaxis.major_label_text_color= "black"
plot_a.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_tick_line_width= 5

ncolumn=int((len(labels))/3)
# print "populations=",len(fids),"pop/column",ncolumn
legend1 = Legend(
    items=leg_1[0:(ncolumn-4)], location=(0, 30))

legend2 = Legend(
    items=leg_1[(ncolumn)-4:(ncolumn*2)-2], location=(0, 30))

legend3 = Legend(
    items=leg_1[(ncolumn*2)-2:], location=(0, 30))

plot_a.add_layout(legend1, 'right')
plot_a.add_layout(legend2, 'right')
plot_a.add_layout(legend3, 'right')

plot_a.legend.location = "top_right"
plot_a.legend.click_policy="hide" # "mute"

plot_a.legend.glyph_width= 18
plot_a.legend.glyph_height= 18

plot_a.legend.label_text_font_style = "normal"
plot_a.legend.label_text_font_size = '10pt'
plot_a.legend.label_width= 8
plot_a.legend.label_height= 8

#Grid lines
plot_a.xgrid.visible = False
plot_a.ygrid.visible = False

plot_a.x_range.flipped = False
plot_a.y_range.flipped = False

plot_a.outline_line_color= 'black'
outline_line_alpha= 1
plot_a.outline_line_width= 2

# Vertical line
vline = Span(location=0, dimension='height', line_color='grey', line_width=1, line_dash='dashed')
# Horizontal line
hline = Span(location=0, dimension='width', line_color='grey', line_width=1, line_dash='dashed')
plot_a.renderers.extend([vline, hline])

plot_a.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [('Population', '@FID'), ('Sample ID', '@IID'),]))

#######################

# PCA Plot 2C

title_b= "Main Figure 2C | PCA for modern and ancient populations"
add_info= "Figure showing modern populations in grey and ancient individuals with colors."

which_pcs= (1,2)
print ('Plotting',['PC' + str(p) + ' ' for p in which_pcs])

# Read table
evec = open(args.input_B)
which_pcs = list(map(int, args.which_pcs.split(',')))

my_eval = open(args.input_B.replace('evec', 'eval'))
eval_per = []
for line in my_eval:
    eval_per.append(float(line.strip()))
eval_per = [x/sum(eval_per)*100 for x in eval_per]

eigs = {}
evec.readline()
evec_all = pd.read_csv(evec, header=None, sep=r'\s+') #, skiprows=1)
pcs = ['ID']
pcs.extend(['PC' + str(x) for x in range(1, evec_all.shape[1]-1)])
pcs.append('PC')
evec_all.columns = pcs
iid_fid = pd.DataFrame(evec_all['ID'].str.split(':').tolist())
df = pd.concat([iid_fid, evec_all], axis=1)
df.rename(columns={0: 'FID', 1: 'IID'}, inplace=True)
source = df
source.set_index('FID')
source  = source.rename(columns={0: "FID", 1: "IID"})
fids = source.FID.unique()

output_file(args.output+'.html', mode='inline')

# Set your own pattern
ifile  = open(args.pattern_B, 'r')
pattern = csv.reader(ifile)
sizes, labels, colours, markers, filling = [], [], [], [], []

for row in pattern:
	sizes.append(row[0])
	labels.append(row[1])
	colours.append(row[2])
	markers.append(row[3])
	filling.append(row[4])
	filling = [d if d!='None' else None for d in filling]

sizes= [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14]

plot_c = figure(title=title_b, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width=1540, height= 800,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_c.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

plot_c.add_layout(caption, "above")
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info, text_font_size='16pt', text_color="black")
plot_c.add_layout(text, 'below')

plot_c.title.text_font_size = '18pt'

#plot_c.xaxis.axis_label="PC1"
plot_c.xaxis.axis_label= "PC"+str(which_pcs[0])+' ('+"%.2f" % eval_per[which_pcs[0]-1]+'% var explained)'
plot_c.xaxis.axis_label_text_font_size = '16pt'
plot_c.xaxis.major_label_text_font_size = '15pt'
plot_c.xaxis.axis_label_text_font= "arial"
plot_c.xaxis.axis_label_text_color= "black"
plot_c.xaxis.major_label_text_color= "black"
plot_c.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_c.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_c.xaxis.major_tick_line_width= 5

#plot_c.yaxis.axis_label="PC2"
plot_c.yaxis.axis_label= "PC"+str(which_pcs[1])+' ('+"%.2f" % eval_per[which_pcs[1]-1]+'% var explained)'
plot_c.yaxis.axis_label_text_font_size = '16pt'
plot_c.yaxis.major_label_text_font_size = '15pt'
plot_c.yaxis.axis_label_text_font= "arial"
plot_c.yaxis.axis_label_text_color= "black"
plot_c.yaxis.major_label_text_color= "black"
plot_c.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_c.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_c.yaxis.major_tick_line_width= 5

ncolumn=int((len(labels))/3+3)
# print "populations=",len(fids),"pop/column",ncolumn
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

legend2 = Legend(
    items=leg_1[ncolumn:ncolumn*2], location=(0, 30))

legend3 = Legend(
    items=leg_1[ncolumn*2:], location=(0, 30))

plot_c.add_layout(legend1, 'right')
plot_c.add_layout(legend2, 'right')
plot_c.add_layout(legend3, 'right')

plot_c.legend.location = "top_right"

plot_c.legend.click_policy="hide" # "mute"

plot_c.legend.glyph_width= 18
plot_c.legend.glyph_height= 18

plot_c.legend.label_text_font_style = "normal"
plot_c.legend.label_text_font_size = '8pt'
plot_c.legend.label_width= 8
plot_c.legend.label_height= 8

#Grid lines
plot_c.xgrid.visible = False
plot_c.ygrid.visible = False

plot_c.x_range.flipped = False
plot_c.y_range.flipped = False

plot_c.outline_line_color= 'black'
outline_line_alpha= 1
plot_c.outline_line_width= 2

# Vertical line
vline = Span(location=0, dimension='height', line_color='grey', line_width=1, line_dash='dashed')
# Horizontal line
hline = Span(location=0, dimension='width', line_color='grey', line_width=1, line_dash='dashed')
plot_c.renderers.extend([vline, hline])

plot_c.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [('Population', '@FID'), ('Sample ID', '@IID'),]))

#######################

# Make a grid
grid= layout([[plot_a],[plot_c]]) #, width=1800, height=700)
show(grid)

# Save plots
print ("Saving Figure 2A and 2C")
export_png(grid, filename=args.output+".png")

# grid.output_backend= "svg"
# export_svgs(grid, filename=args.output+".svg")

exit()

#######################

