"""
Plotting script for Suppl. Figure 5
"""
__author__ = 'Cesar Fortes-Lima'

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import numpy as np
import sys, random, csv
import warnings
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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input', default='Tables/Fulani-World_DB.evec') #assumes eval in same place
parser.add_argument('-p', '--pattern', default='Tables/Fulani-World_DB_pca.csv')
parser.add_argument('-o', '--output', default='02-Suppl_Figures/Figure_S05')
# Optional
parser.add_argument('--title', default='Figure S5 | PCA for modern and ancient individuals')
parser.add_argument('--which_pcs', default='1,2')
args = parser.parse_args()

# Usage: 
# DB='Tables/Fulani-World_DB'
# python3 scripts/bokeh_Figure_S5.py -i ${DB}.pca.evec -p ${DB}_pca.csv -o 02-Suppl_Figures/Figure_S05
#

# Read table
evec = open(args.input)
which_pcs = list(map(int, args.which_pcs.split(',')))

my_eval = open(args.input.replace('evec', 'eval'))
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
ifile  = open(args.pattern, 'r')
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

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption= Label(text=' Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).', **label_opts)

####################

# PCA Plot S5A

title_b= "Figure S5A | PC1 vs PC2"
which_pcs= (1,2)
print ('Plotting',['PC' + str(p) + ' ' for p in which_pcs])

plot_a = figure(title=title_b, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width=1600, height= 800,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_a.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

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
    items=leg_1[0:ncolumn], location=(0, 30))

legend2 = Legend(
    items=leg_1[ncolumn:ncolumn*2], location=(0, 30))

legend3 = Legend(
    items=leg_1[ncolumn*2:], location=(0, 30))

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

# PCA Plot S5B

title_a= "PC1 vs PC3"
which_pcs= (1,3)
print ('Plotting',['PC' + str(p) + ' ' for p in which_pcs])

plot_b = figure(title=title_a, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width=900, height= 800,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_b.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

plot_b.title.text_font_size = '18pt'

#plot_b.xaxis.axis_label="PC1"
plot_b.xaxis.axis_label= "PC"+str(which_pcs[0])+' ('+"%.2f" % eval_per[which_pcs[0]-1]+'% var explained)'
plot_b.xaxis.axis_label_text_font_size = '16pt'
plot_b.xaxis.major_label_text_font_size = '15pt'
plot_b.xaxis.axis_label_text_font= "arial"
plot_b.xaxis.axis_label_text_color= "black"
plot_b.xaxis.major_label_text_color= "black"
plot_b.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_tick_line_width= 5

#plot_b.yaxis.axis_label="PC2"
plot_b.yaxis.axis_label= "PC"+str(which_pcs[1])+' ('+"%.2f" % eval_per[which_pcs[1]-1]+'% var explained)'
plot_b.yaxis.axis_label_text_font_size = '16pt'
plot_b.yaxis.major_label_text_font_size = '15pt'
plot_b.yaxis.axis_label_text_font= "arial"
plot_b.yaxis.axis_label_text_color= "black"
plot_b.yaxis.major_label_text_color= "black"
plot_b.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_tick_line_width= 5

#Grid lines
plot_b.xgrid.visible = False
plot_b.ygrid.visible = False

plot_b.x_range.flipped = False
plot_b.y_range.flipped = False

plot_b.outline_line_color= 'black'
outline_line_alpha= 1
plot_b.outline_line_width= 2

# Vertical line
vline = Span(location=0, dimension='height', line_color='grey', line_width=1, line_dash='dashed')
# Horizontal line
hline = Span(location=0, dimension='width', line_color='grey', line_width=1, line_dash='dashed')
plot_b.renderers.extend([vline, hline])

plot_b.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [('Population', '@FID'), ('Sample ID', '@IID'),]))

#######################

# PCA Plot S5C
title_c= "PC1 vs PC4"
which_pcs= (1,4)
print ('Plotting',['PC' + str(p) + ' ' for p in which_pcs])

plot_c = figure(title=title_c, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width=900, height= 800,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_c.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

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

# PCA Plot S5D
title_c= "PC1 vs PC5"
which_pcs= (1,5)
print ('Plotting',['PC' + str(p) + ' ' for p in which_pcs])

plot_d = figure(title=title_c, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width=900, height= 800,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_d.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

plot_d.title.text_font_size = '18pt'

#plot_d.xaxis.axis_label="PC1"
plot_d.xaxis.axis_label= "PC"+str(which_pcs[0])+' ('+"%.2f" % eval_per[which_pcs[0]-1]+'% var explained)'
plot_d.xaxis.axis_label_text_font_size = '16pt'
plot_d.xaxis.major_label_text_font_size = '15pt'
plot_d.xaxis.axis_label_text_font= "arial"
plot_d.xaxis.axis_label_text_color= "black"
plot_d.xaxis.major_label_text_color= "black"
plot_d.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_d.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_d.xaxis.major_tick_line_width= 5

#plot_d.yaxis.axis_label="PC2"
plot_d.yaxis.axis_label= "PC"+str(which_pcs[1])+' ('+"%.2f" % eval_per[which_pcs[1]-1]+'% var explained)'
plot_d.yaxis.axis_label_text_font_size = '16pt'
plot_d.yaxis.major_label_text_font_size = '15pt'
plot_d.yaxis.axis_label_text_font= "arial"
plot_d.yaxis.axis_label_text_color= "black"
plot_d.yaxis.major_label_text_color= "black"
plot_d.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_d.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_d.yaxis.major_tick_line_width= 5

#Grid lines
plot_d.xgrid.visible = False
plot_d.ygrid.visible = False

plot_d.x_range.flipped = False
plot_d.y_range.flipped = False

plot_d.outline_line_color= 'black'
outline_line_alpha= 1
plot_d.outline_line_width= 2

# Vertical line
vline = Span(location=0, dimension='height', line_color='grey', line_width=1, line_dash='dashed')
# Horizontal line
hline = Span(location=0, dimension='width', line_color='grey', line_width=1, line_dash='dashed')
plot_d.renderers.extend([vline, hline])

plot_d.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [('Population', '@FID'), ('Sample ID', '@IID'),]))

plot_d.add_layout(caption, "below")

#######################

# PCA Plot S5E

title_c= "PC1 vs PC6"
which_pcs= (1,6)
print ('Plotting',['PC' + str(p) + ' ' for p in which_pcs])

plot_e = figure(title=title_c, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]), y_axis_label="PC"+str(which_pcs[1]), width=900, height= 800,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_e.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

plot_e.title.text_font_size = '18pt'

#plot_e.xaxis.axis_label="PC1"
plot_e.xaxis.axis_label= "PC"+str(which_pcs[0])+' ('+"%.2f" % eval_per[which_pcs[0]-1]+'% var explained)'
plot_e.xaxis.axis_label_text_font_size = '16pt'
plot_e.xaxis.major_label_text_font_size = '15pt'
plot_e.xaxis.axis_label_text_font= "arial"
plot_e.xaxis.axis_label_text_color= "black"
plot_e.xaxis.major_label_text_color= "black"
plot_e.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_e.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_e.xaxis.major_tick_line_width= 5

#plot_e.yaxis.axis_label="PC2"
plot_e.yaxis.axis_label= "PC"+str(which_pcs[1])+' ('+"%.2f" % eval_per[which_pcs[1]-1]+'% var explained)'
plot_e.yaxis.axis_label_text_font_size = '16pt'
plot_e.yaxis.major_label_text_font_size = '15pt'
plot_e.yaxis.axis_label_text_font= "arial"
plot_e.yaxis.axis_label_text_color= "black"
plot_e.yaxis.major_label_text_color= "black"
plot_e.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_e.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_e.yaxis.major_tick_line_width= 5

#Grid lines
plot_e.xgrid.visible = False
plot_e.ygrid.visible = False

plot_e.x_range.flipped = False
plot_e.y_range.flipped = False

plot_e.outline_line_color= 'black'
outline_line_alpha= 1
plot_e.outline_line_width= 2

# Vertical line
vline = Span(location=0, dimension='height', line_color='grey', line_width=1, line_dash='dashed')
# Horizontal line
hline = Span(location=0, dimension='width', line_color='grey', line_width=1, line_dash='dashed')
plot_e.renderers.extend([vline, hline])

plot_e.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [('Population', '@FID'), ('Sample ID', '@IID'),]))

#######################

# Make a grid
grid= layout([[plot_a] ,[plot_b, plot_c], [plot_d, plot_e]]) #, width=1800, height=700)
show(grid)

# Save plots
print ("Saving Figure S5")
export_png(grid, filename=args.output+".png")

# grid.output_backend= "svg"
# export_svgs(grid, filename=args.output+".svg")

exit()

#######################

