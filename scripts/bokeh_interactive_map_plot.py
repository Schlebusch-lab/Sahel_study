"""
Interactive plots for maps
"""
__author__ = 'Cesar Fortes-Lima'

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import pandas as pd
import argparse, pdb
import sys, random, csv
from tabulate import tabulate

from bokeh.io.export import export_svgs, export_png
from bokeh.io import output_notebook
from bokeh.plotting import figure, show, output_file, ColumnDataSource
#from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import Spectral, RdYlBu, RdYlGn
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column
from bokeh.models import Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input', default='', help='input file') #assumes eval in same place
parser.add_argument('-o', '--output', help='uses .png or .pdf suffix to determine type of file to plot')
parser.add_argument('--title', default='')

args = parser.parse_args()

# Usage
# python bokeh_interactive_map_plot.py Bantu_df.csv

# pdb.set_trace()

df= pd.read_csv(args.input, index_col= 0)
#df= pd.read_csv("pattern3.csv", index_col= 0)
df.head()


# Select type of map to use (see: https://docs.bokeh.org/en/2.4.0/docs/reference/tile_providers.html)
#chosentile= get_provider(Vendors.OSM)
#chosentile= add_tile(Vendors.CARTODBPOSITRON_RETINA)

# Define function to switch from lat/long to mercator coordinates
def x_coord(x, y):
	lat= x
	lon= y 
	r_major= 6378137.000
	x= r_major * np.radians(lon)
	scale= x/lon
	y= 180.0/np.pi * np.log(np.tan(np.pi/4.0 + lat * (np.pi/180.0)/2.0)) * scale
	return (x, y)

# Define coord as tuple (lat,long)
df['coordinates']= list(zip(df['Latitude'], df['Longitude']))

# Population	Colour	Shape	Filling

# Obtain list of mercator coordinates
mercators= [x_coord(x, y) for x, y in df['coordinates'] ]

# Create mercator column in our df
df['mercator']= mercators

# Split that column out into two separate columns - mercator_x and mercator_y
df[['mercator_x', 'mercator_y']]= df['mercator'].apply(pd.Series)


# Examine our modified DataFrame
df.head()
# Tell Bokeh to use df as the source of the data
source= ColumnDataSource(data= df)

# Define color mapper - which column will define the colour of the data points
#color_mapper= linear_cmap(field_name= 'Latitude', palette= palette, low= df['Latitude'].min(), high= df['Latitude'].max())
palette= df['Colour']

# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful
#tooltips= [("Population","@Population"), ("Sample ID","@Sample")]
tooltips= [("Group","@Group"), ("Population","@Population"), ("Sample size","@N")]

output_file("tile.html")

# Create figure
plot= figure(title= args.title, toolbar_location="above", x_axis_type= "mercator", x_axis_label= 'Longitude', y_axis_type= "mercator", y_axis_label= 'Latitude', # , x_range=(-2000000, 6000000), y_range=(-1000000, 7000000))
	tooltips= tooltips, width = 800, height = 600,
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')

# title= args.title, 
# pdb.set_trace()

# Add map tile
# plot.add_tile(chosentile)
plot.add_tile("CartoDB Positron", retina=True)

#Grid lines
plot.xgrid.visible = False
plot.ygrid.visible = False

# Add points using mercator coordinates
plot.scatter(source= source, x= 'mercator_x', y= 'mercator_y', color=  'Colour', marker= 'Shape', fill_color= 'Filling', 
	size= 20, fill_alpha= 1, muted_alpha= 0, line_width= 3)

#Defines color bar
#color_bar= ColorBar(color_mapper= color_mapper['transform'],
#	formatter= NumeralTickFormatter(format= '0.0[0000]'), label_standoff= 13, width= 8, location= (0,0))

# Set color_bar location
#plot.add_layout(color_bar, 'right')

plot.title.text_font_size = '20pt'
#plot.xaxis.axis_label="PC1"
plot.xaxis.axis_label_text_font_size = "20pt"
plot.xaxis.major_label_text_font_size = "15pt"
plot.xaxis.axis_label_text_font= "arial"
plot.xaxis.axis_label_text_color= "black"
plot.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.xaxis.major_tick_line_width= 5

#plot.yaxis.axis_label="PC2"
plot.yaxis.axis_label_text_font_size = "20pt"
plot.yaxis.major_label_text_font_size = "18pt"
plot.yaxis.axis_label_text_font= "arial"
plot.yaxis.axis_label_text_color= "black"
plot.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot.yaxis.major_tick_line_width= 5

plot.outline_line_color= 'black'
outline_line_alpha= 1
plot.outline_line_width= 2


out=args.output

# Show the tabbed layout and Save plot
#export_png(plot, filename=out+".png")
plot.output_backend= "svg"
export_svgs(plot, filename="Map.svg")

show(plot)
exit()

###########################################

