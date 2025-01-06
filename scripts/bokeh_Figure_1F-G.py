"""
Plotting script for Main Figure 1F and 1G
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
parser.add_argument('--input', default='Tables/Fulani_PCA-UMAP_table.txt') #assumes eval in same place
parser.add_argument('--output', default='02-Suppl_Figures/Main_Figure_1F-G')
parser.add_argument('--pattern_A', default='Tables/Fulani_PCA-UMAP_pattern_A.csv')
parser.add_argument('--pattern_B', default='Tables/Fulani_PCA-UMAP_pattern_B.csv')
# Optional
parser.add_argument('--umap', default='1,2')
parser.add_argument('--title', default='')
args = parser.parse_args()

# Usage: 
# Table_A='Tables/Fulani-World_DB'
# Table_B='Tables/Fulani_aDNA-Modern_DB'
#
# python3 scripts/bokeh_Figure_1F-G.py --input Tables/Fulani_PCA-UMAP_table.txt --output 01-Main_Figures/Figure_1F-G
# --pattern_A Tables/Fulani_PCA-UMAP_pattern_A.csv --pattern_B Tables/Fulani_PCA-UMAP_pattern_B.csv
#

####################

# PCA Plot 1F
title_a= "Figure 1F | PCA-UMAP on the basis of Fulani and other Western and Central African populations"
umap= (1,2)
print ('Plotting',['UMAP' + str(p) + ' ' for p in umap])

# Read table
evec = open(args.input)
umap = list(map(int, args.umap.split(',')))

eigs = {}
evec.readline()
evec_all = pd.read_csv(evec, header=None, sep=r'\s+')
pcs = ['ID']
pcs.extend(['UMAP' + str(x) for x in range(1, evec_all.shape[1]-1)])
pcs.append('UMAP2')
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

plot_a = figure(title=title_a, toolbar_location="above", x_axis_label="PC"+str(umap[0]), y_axis_label="PC"+str(umap[1]), width=1300, height= 740,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append((pop, [plot_a.scatter(x='UMAP'+str(umap[0]), y='UMAP'+str(umap[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption= Label(text=' Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).', **label_opts)
plot_a.add_layout(caption, "above")
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text='\n', text_font_size='16pt', text_color="white")
plot_a.add_layout(text, 'below')
plot_a.title.text_font_size = '18pt'

plot_a.xaxis.axis_label= "UMAP"+str(umap[0])
plot_a.xaxis.axis_label_text_font_size = '16pt'
plot_a.xaxis.major_label_text_font_size = '15pt'
plot_a.xaxis.axis_label_text_font= "arial"
plot_a.xaxis.axis_label_text_color= "black"
plot_a.xaxis.major_label_text_color= "black"
plot_a.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_tick_line_width= 5

plot_a.yaxis.axis_label= "UMAP"+str(umap[1])
plot_a.yaxis.axis_label_text_font_size = '16pt'
plot_a.yaxis.major_label_text_font_size = '15pt'
plot_a.yaxis.axis_label_text_font= "arial"
plot_a.yaxis.axis_label_text_color= "black"
plot_a.yaxis.major_label_text_color= "black"
plot_a.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_tick_line_width= 5

ncolumn=int((len(labels))/2)
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

legend2 = Legend(
    items=leg_1[ncolumn:], location=(0, 30))

plot_a.add_layout(legend1, 'right')
plot_a.add_layout(legend2, 'right')

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

plot_a.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [('Population', '@FID'), ('Sample ID', '@IID'),]))

#######################

# PCA Plot 1G

title_b= "Figure 1G | PCA-UMAP on the basis of Fulani and other Western and Central African populations"

umap= (1,2)
print ('Plotting',['UMAP' + str(p) + ' ' for p in umap])
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

sizes= [10]
while len(sizes) < len(fids):
	sizes.extend(sizes)
	sizes=sizes[0:len(fids)]

plot_b = figure(title=title_b, toolbar_location="above", x_axis_label="PC"+str(umap[0]), y_axis_label="PC"+str(umap[1]), width=1300, height= 700,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom', background_fill_color="#fafafa", output_backend="svg")

leg_1 = []
for counter,pop in enumerate(labels):
	leg_1.append(( pop, [plot_b.scatter(x='UMAP'+str(umap[0]), y='UMAP'+str(umap[1]), source=source.loc[source['FID'] == pop],
		marker=markers[counter], size=int(sizes[counter]), color=colours[counter], muted_alpha=0.5, fill_color=filling[counter] ) ] ))

plot_b.add_layout(caption, "above")
plot_b.title.text_font_size = '18pt'

plot_b.xaxis.axis_label= "UMAP"+str(umap[0])
plot_b.xaxis.axis_label_text_font_size = '16pt'
plot_b.xaxis.major_label_text_font_size = '15pt'
plot_b.xaxis.axis_label_text_font= "arial"
plot_b.xaxis.axis_label_text_color= "black"
plot_b.xaxis.major_label_text_color= "black"
plot_b.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_tick_line_width= 5

plot_b.yaxis.axis_label= "UMAP"+str(umap[1])
plot_b.yaxis.axis_label_text_font_size = '16pt'
plot_b.yaxis.major_label_text_font_size = '15pt'
plot_b.yaxis.axis_label_text_font= "arial"
plot_b.yaxis.axis_label_text_color= "black"
plot_b.yaxis.major_label_text_color= "black"
plot_b.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_tick_line_width= 5

ncolumn=int((len(labels))/2)
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

legend2 = Legend(
    items=leg_1[ncolumn:], location=(0, 30))

plot_b.add_layout(legend1, 'right')
plot_b.add_layout(legend2, 'right')

plot_b.legend.location = "top_right"
plot_b.legend.click_policy="hide" # "mute"

plot_b.legend.glyph_width= 18
plot_b.legend.glyph_height= 18

plot_b.legend.label_text_font_style = "normal"
plot_b.legend.label_text_font_size = '10pt'
plot_b.legend.label_width= 8
plot_b.legend.label_height= 8

#Grid lines
plot_b.xgrid.visible = False
plot_b.ygrid.visible = False

plot_b.x_range.flipped = False
plot_b.y_range.flipped = False

plot_b.outline_line_color= 'black'
outline_line_alpha= 1
plot_b.outline_line_width= 2

plot_b.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [('Population', '@FID'), ('Sample ID', '@IID'),]))

#######################

# Make a grid
grid= layout([[plot_a],[plot_b]]) #, width=1800, height=700)
show(grid)

# Save plots
print ("Saving Figure 1F and 1G")
export_png(grid, filename=args.output+".png")

# grid.output_backend= "svg"
# export_svgs(grid, filename=args.output+".svg")

exit()

#######################

