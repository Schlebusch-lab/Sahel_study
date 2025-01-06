"""
Interactive plots for maps included in Figure S3
"""
__author__ = 'Cesar Fortes-Lima'

import numpy as np
import pandas as pd
import argparse, pdb
import sys, random, csv
from tabulate import tabulate

# Bokeh imports
from bokeh.io.export import export_svgs, export_png
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column, gridplot
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.models import Label, Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('--input_A', default="Tables/Fulani-World_DB.map.csv", help='input file')
parser.add_argument('--input_B', default="Tables/Fulani_aDNA-Modern_DB.map.csv", help='input file')
parser.add_argument('--output', default="02-Suppl_Figures/Figure_S03", help='output files')
args = parser.parse_args()

# Usage:
# python3 scripts/bokeh_Figure_S3.py --output 02-Suppl_Figures/Figure_S03 \
# --input_A Tables/Fulani-World_DB.map.csv --input_B Tables/Fulani_aDNA-Modern_DB.map.csv
#

# Define function to switch from lat/long to mercator coordinates
def x_coord(x, y):
	lat= x
	lon= y 
	r_major= 6378137.000
	x= r_major * np.radians(lon)
	scale= x/lon
	y= 180.0/np.pi * np.log(np.tan(np.pi/4.0 + lat * (np.pi/180.0)/2.0)) * scale
	return (x, y)


#########################

# Figure S3A. First map.

title_a= "Figure S3A | Distribution of modern populations included in this study"
add_info_a= "Map showing all the populations included in the 'Fulani-World' dataset (Table S2)."

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption= Label(text=' Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).', **label_opts)
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_a, text_font_size='16pt', text_color="black")

df= pd.read_csv(args.input_A, index_col= 0)
source = df
source.set_index('Population')
fids = source.Population.unique()
labels = fids

# Define coord as tuple (lat,long)
df['coordinates']= list(zip(df['Latitude'], df['Longitude']))

# Obtain list of mercator coordinates
mercators= [x_coord(x, y) for x, y in df['coordinates'] ]

# Create mercator column in our df
df['mercator']= mercators

# Split that column out into two separate columns - mercator_x and mercator_y
df[['mercator_x', 'mercator_y']]= df['mercator'].apply(pd.Series)

tooltips = [("Group","@Group"), ("Population","@Population"), ("N_samples","@N")]

# Create figure
output_file(args.output+'.html', mode='inline')
plot_a= figure(title= title_a, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', 
	tooltips= tooltips, height= 700, width= 1300,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')

# Select type of map to use (see: https://docs.bokeh.org/en/2.4.0/docs/reference/tile_providers.html)
# Add map tile
plot_a.add_tile("CartoDB Positron", retina=True)

# Add points using mercator coordinates
# p.circle(x= 'mercator_x', y= 'mercator_y', color= color_mapper, source= source, size= 30, fill_alpha= 0.7)
leg_1 = []

for counter,pop in enumerate(labels):
	#labels.append(pop)
	leg_1.append((pop, [plot_a.scatter(x= 'mercator_x', y= 'mercator_y', source=source.loc[source['Population'] == pop], color= 'Colour', marker= 'Shape', fill_color= 'Filling', 
	fill_alpha= 1, size= 22, muted_alpha= 0, line_width= 2) ] ))

plot_a.add_layout(caption, "above")
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text='\n', text_font_size='16pt', text_color="white")
plot_a.add_layout(text, 'below')

# Set color_bar location
#plot_a.add_layout(color_bar, 'right')

plot_a.title.text_font_size = '20pt'

#plot_a.xaxis.axis_label="Longitude"
plot_a.xaxis.axis_label_text_font_size = "18pt"
plot_a.xaxis.major_label_text_font_size = "15pt"
plot_a.xaxis.axis_label_text_font= "arial"
plot_a.xaxis.axis_label_text_color= "black"
plot_a.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_tick_line_width= 5

#plot_a.yaxis.axis_label="Latitude"
plot_a.yaxis.axis_label_text_font_size = "18pt"
plot_a.yaxis.major_label_text_font_size = "15pt"
plot_a.yaxis.axis_label_text_font= "arial"
plot_a.yaxis.axis_label_text_color= "black"
plot_a.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_tick_line_width= 5

#Grid lines
plot_a.xgrid.visible = False
plot_a.ygrid.visible = False

plot_a.outline_line_color= 'black'
outline_line_alpha= 1
plot_a.outline_line_width= 2

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
plot_a.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [("Group","@Group"), ("Population","@Population"), ("N_samples","@N")]))

ncolumn=int((len(labels))/3+1)
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
plot_a.legend.label_text_font_size = '8pt'
plot_a.legend.label_width= 8
plot_a.legend.label_height= 8


#######################

# Figure S3B. Second map.

title_b= "Figure S3B | Distribution of ancient populations included in this study"
add_info_b= "Map showing all the populations included in the 'Fulani_aDNA-Modern' dataset (Table S3)."

text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_b, text_font_size='16pt', text_color="black")

df= pd.read_csv(args.input_B, index_col= 0)
source = df
source.set_index('Population')
fids = source.Population.unique()
labels = fids

# Define coord as tuple (lat,long)
df['coordinates']= list(zip(df['Latitude'], df['Longitude']))

# Obtain list of mercator coordinates
mercators= [x_coord(x, y) for x, y in df['coordinates'] ]

# Create mercator column in our df
df['mercator']= mercators

# Split that column out into two separate columns - mercator_x and mercator_y
df[['mercator_x', 'mercator_y']]= df['mercator'].apply(pd.Series)

tooltips = [("Population","@Population"), ("Sample","@Sample")]

# Create figure
output_file(args.output+'.html', mode='inline')
plot_b= figure(title= title_b, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', 
	tooltips= tooltips, height= 550, width= 1300,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')

plot_b.add_layout(caption, "above")
plot_b.add_layout(text, 'below')
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text= add_info_b, text_font_size='16pt', text_color="white")
plot_b.add_layout(text, 'below')

# Select type of map to use (see: https://docs.bokeh.org/en/2.4.0/docs/reference/tile_providers.html)
# Add map tile
plot_b.add_tile("CartoDB Positron", retina=True)

# Add points using mercator coordinates
leg_1 = []

for counter,pop in enumerate(labels):
	#labels.append(pop)
	leg_1.append((pop, [plot_b.scatter(x= 'mercator_x', y= 'mercator_y', source=source.loc[source['Population'] == pop], color= 'Colour', marker= 'Shape', fill_color= 'Filling', 
	fill_alpha= 1, size= 22, muted_alpha= 0, line_width= 2) ] ))

# Set color_bar location
#plot_b.add_layout(color_bar, 'right')

plot_b.title.text_font_size = '20pt'

#plot_b.xaxis.axis_label="Longitud"
plot_b.xaxis.axis_label_text_font_size = "18pt"
plot_b.xaxis.major_label_text_font_size = "15pt"
plot_b.xaxis.axis_label_text_font= "arial"
plot_b.xaxis.axis_label_text_color= "black"
plot_b.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_tick_line_width= 5

#plot_b.yaxis.axis_label="Latitude"
plot_b.yaxis.axis_label_text_font_size = "18pt"
plot_b.yaxis.major_label_text_font_size = "15pt"
plot_b.yaxis.axis_label_text_font= "arial"
plot_b.yaxis.axis_label_text_color= "black"
plot_b.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_tick_line_width= 5

#Grid lines
plot_b.xgrid.visible = False
plot_b.ygrid.visible = False

plot_b.outline_line_color= 'black'
outline_line_alpha= 1
plot_b.outline_line_width= 2

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
plot_b.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [("Population","@Population"), ("Sample","@Sample")]))

ncolumn=int((len(labels))/3+1)
# print "populations=",len(fids),"pop/column",ncolumn
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

legend2 = Legend(
    items=leg_1[ncolumn:ncolumn*2], location=(0, 30))

legend3 = Legend(
    items=leg_1[ncolumn*2:], location=(0, 30))

plot_b.add_layout(legend1, 'right')
plot_b.add_layout(legend2, 'right')
plot_b.add_layout(legend3, 'right')

plot_b.legend.location = "top_right"
plot_b.legend.click_policy="hide" # "mute"

plot_b.legend.glyph_width= 18
plot_b.legend.glyph_height= 18

plot_b.legend.label_text_font_style = "normal"
plot_b.legend.label_text_font_size = '8pt'
plot_b.legend.label_width= 8
plot_b.legend.label_height= 8

#######################

# Make a grid
grid= gridplot([[plot_a], [plot_b]]) #, width=250, height=250)

# Save plots
print ("Saving Figure S3")
export_png(grid, filename=args.output+".png")
show(grid)

# plot_a.output_backend= "svg"
# export_svgs(plot_a, filename=args.output+"_S3A.svg")

# plot_b.output_backend= "svg"
# export_svgs(plot_b, filename=args.output+"_S3B.svg")

exit()

#######################
