#!/usr/bin/python
"""
Plotting script for Suppl Figure S21
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

import pdb
from io import StringIO
from tabulate import tabulate

# Bokeh imports
from bokeh.io.export import export_svgs, export_png
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, gridplot, layout
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Label, Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import inferno, Spectral6

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('--input_A', default='Tables/Only-Fulani_DB.ROH_Class_table.txt')
parser.add_argument('--input_B', default='Tables/Fulani-World_DB.ROH_Class_table.txt')
parser.add_argument('-o', '--output', default='02-Suppl_Figures/Figure_S21')

args = parser.parse_args()

#pdb.set_trace()

# Usage: 
# python3 scripts/bokeh_Figure_S21.py --output "02-Suppl_Figures/Figure_S21"
# --input_A "Tables/Only-Fulani_DB.ROH_Class_table.txt" --input_B "Tables/Fulani-World_DB.ROH_Class_table.txt

output_file(args.output+'.html', mode='inline')

# Plot only for Fulani populations
title='Figure S21A | Categories of ROH length on the basis of the Only-Fulani dataset'

source = pd.read_csv(args.input_A, header=None, sep='\t')
source  = source.rename(columns={0: "Population", 1: "Class", 2: "Mean"})
Populations = source.Population.unique()

leg_0 = []
leg_1 = []
labels = ['Mauritania_Fulani_Assaba','Senegal_Fulani_Linguere','Senegal_Halpularen','Gambia_Fula','Guinea_Fulani','Mali_Fulani_Diafarabe','Mali_Fulani_InnerDelta','BurkinaFaso_Fulani_Banfora','BurkinaFaso_Fulani_Tindangou','BurkinaFaso_Fulani_Ziniare','Niger_Fulani_Abalak','Niger_Fulani_Ader','Niger_Fulani_Balatungur','Niger_Fulani_Diffa','Niger_Fulani_Zinder','Cameroon_Fulani_Tcheboua','Chad_Fulani_Bongor','Chad_Fulani_Linia']
markers = ['x','circle','cross','triangle','diamond','inverted_triangle','asterisk','square_x','circle_cross','diamond_cross','circle_x','square_cross','triangle','square','square','circle','circle','diamond']
colours = ['#66AEBF','#3B9AB2','#57A7BA','#49A0B6','#74B5C3','#8CBAA9','#C2C460','#A7BF85','#E9C825','#DDC93C','#E5BA11','#E7C11B','#E58300','#E2A600','#E2B407','#E58300','#F21A00','#EE3D00']
filling = ['white','white','white','white','white','white','white','white','white','white','white','white','#E58300','#E2A600','white','#E58300','white','#EE3D00']

plot_a = figure(title=title, toolbar_location="above", x_axis_label="ROH length category",y_axis_label="Mean total length of ROH (Mb)", width = 1500, height = 700, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')

for counter,pop in enumerate(labels):
	leg_0.append(( pop, [plot_a.line(x='Class', y='Mean', source=source.loc[source['Population'] == pop], color=colours[counter], line_width=3, muted_alpha=0.2 ) ] ))
	leg_1.append(( pop, [plot_a.scatter(x='Class', y='Mean', source=source.loc[source['Population'] == pop],
		marker=markers[counter], size=15, color=colours[counter], muted_alpha=0.6, fill_color=filling[counter] ) ] ))

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption= Label(text=' Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).', **label_opts)
plot_a.add_layout(caption, "above")
text= Label(x= 0, y= 0, x_units='screen', y_units='screen', text='\n', text_font_size='16pt', text_color="white")
plot_a.add_layout(text, 'below')
plot_a.title.text_font_size = '18pt'

plot_a.xaxis.major_label_overrides = {1: '[0.3-0.5Mb)', 2:'[0.5-1Mb)', 3:'[1-2Mb)', 4:'[2-4Mb)', 5:'[4-8Mb)', 6:'[8-16Mb)' }
plot_a.xaxis.axis_label="ROH length category"
plot_a.xaxis.axis_label_text_font_size = "17pt"
plot_a.xaxis.major_label_text_font_size = "13pt"
plot_a.xaxis.axis_label_text_font= "arial"
plot_a.xaxis.axis_label_text_color= "black"
plot_a.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.xaxis.major_tick_line_width= 5

plot_a.yaxis.axis_label="Mean total length of ROH (Mb)"
plot_a.yaxis.axis_label_text_font_size = "17pt"
plot_a.yaxis.major_label_text_font_size = "15pt"
plot_a.yaxis.axis_label_text_font= "arial"
plot_a.yaxis.axis_label_text_color= "black"
plot_a.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_a.yaxis.major_tick_line_width= 5

#Grid lines
plot_a.xgrid.visible = False
plot_a.xgrid.grid_line_alpha = 0.8
plot_a.xgrid.grid_line_dash = [6, 4]
plot_a.ygrid.visible = False
plot_a.ygrid.grid_line_alpha = 0.8
plot_a.ygrid.grid_line_dash = [6, 4]

#Legend
ncolumn=int((len(Populations))/2)
legend1 = Legend(
    items=leg_0[0:ncolumn], location=(0, 30),)

legend2 = Legend(
    items=leg_0[ncolumn:], location=(0, 30))

legend3 = Legend(
    items=leg_0[ncolumn*2:ncolumn*3], location=(0, 30))

legend4 = Legend(
    items=leg_0[ncolumn*3:], location=(0, 30))

plot_a.add_layout(legend1, 'right')
plot_a.add_layout(legend2, 'right')
plot_a.add_layout(legend3, 'right')
plot_a.add_layout(legend4, 'right')

plot_a.legend.location = "top_right"
plot_a.legend.click_policy="hide"#"mute"
plot_a.legend.label_text_font_size = '8pt'

plot_a.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [
	 ('Population:', '@Population'),
		 ]
	 ))


#######################

# Plot for Fulani and reference populations

title='Figure S21B | Categories of ROH length on the basis of the Fulani-World dataset'

source = pd.read_csv(args.input_B, header=None, sep='\t')
source  = source.rename(columns={0: "Population", 1: "Class", 2: "Mean"})
Populations = source.Population.unique()

leg_0 = []
leg_1 = []
labels= ['Mauritania_Fulani_Assaba','Senegal_Fulani_Linguere','Senegal_Halpularen','Gambia_Fula','Guinea_Fulani','Mali_Fulani_Diafarabe','Mali_Fulani_InnerDelta','BurkinaFaso_Fulani_Banfora','BurkinaFaso_Fulani_Tindangou','BurkinaFaso_Fulani_Ziniare','Niger_Fulani_Abalak','Niger_Fulani_Ader','Niger_Fulani_Balatungur','Niger_Fulani_Diffa','Niger_Fulani_Zinder','Cameroon_Fulani_Tcheboua','Chad_Fulani_Bongor','Chad_Fulani_Linia','Senegal_Bedik','Gambia_GWD','Gambia_Jola','Gambia_Wolof','Gambia_Mandinka','SierraLeone_MSL','BurkinaFaso_Gurmantche','BurkinaFaso_Gurunsi','BurkinaFaso_Mossi','IvoryCoast_Ahizi','IvoryCoast_Yacouba','Ghana_GaAdangbe','Mali_Bwa','Benin_Fon','Benin_Yoruba','Benin_Bariba','Nigeria_Igbo','Nigeria_YRI','Nigeria_ESN','Chad_Daza','Chad_Kanembu','Chad_Laal','Chad_Sara','Chad_Toubou','Sudan_Daju','Sudan_NubaKoalib','Sudan_Nubian','Sudan_Zaghawa','Ethiopia_Gumuz','Ethiopia_Amhara','Ethiopia_Oromo','Ethiopia_Wolayta','Ethiopia_Somali','Morocco_BerberAsni','Morocco_BerberBouhria','Morocco_BerberFiguig','Egypt_Egyptian','Lebanon_LebaneseChristian','Lebanon_LebaneseDruze','Lebanon_LebaneseMuslim','Yemen_Yemeni','Europe_TSI','Europe_IBS','Europe_SpainGranada','Europe_SpainHuelva','Europe_SouthPortugal','Europe_CEU','Europe_GBR']
colours= ['#66AEBF','#3B9AB2','#57A7BA','#49A0B6','#74B5C3','#8CBAA9','#C2C460','#A7BF85','#E9C825','#DDC93C','#E5BA11','#E7C11B','#E58300','#E2A600','#E2B407','#E58300','#F21A00','#EE3D00','#004529','#ADDD8E','#78C679','#238443','#41AB5D','#ADDD8E','#238443','#006837','#004529','#004529','#ADDD8E','#006837','#78C679','#78C679','#41AB5D','#ADDD8E','#238443','#006837','#41AB5D','#543005','#8C510A','#BF812D','#DFC27D','#543005','#8C510A','#BF812D','#DFC27D','#543005','#BF812D','#DFC27D','#543005','#DFC27D','#8C510A','tan','tan','tan','tan','skyblue','skyblue','skyblue','skyblue','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray']
markers= ['x','circle','cross','triangle','diamond','inverted_triangle','asterisk','square_x','circle_cross','diamond_cross','circle_x','square_cross','triangle','square','square','circle','circle','diamond','square_cross','triangle','cross','x','diamond','inverted_triangle','square','circle_x','square_cross','diamond_cross','asterisk','square','circle_cross','circle','triangle','diamond','cross','circle','triangle','asterisk','x','square_x','diamond','inverted_triangle','circle_cross','square_cross','circle_x','diamond_cross','square','triangle','square','circle','diamond','circle','triangle','cross','x','diamond','inverted_triangle','square_x','asterisk','circle','square_cross','circle_cross','circle_x','diamond_cross','square','square']
filling= [None,None,None,None,None,None,None,None,None,None,None,None,'#E58300','#E2A600',None,'#E58300',None,'#EE3D00',None,None,None,None,None,None,'#238443',None,None,None,None,None,None,'#78C679',None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,'#8C510A','#DFC27D','#8C510A','#543005',None,None,None,None,None,None,None,None,'#737373',None,None,None,None,'#737373',None]

plot_b = figure(title=title, toolbar_location="above", x_axis_label="ROH length category",y_axis_label="Mean total length of ROH (Mb)", width = 1790, height = 700, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')

for counter,pop in enumerate(labels):
	leg_0.append(( pop, [plot_b.line(x='Class', y='Mean', source=source.loc[source['Population'] == pop], color=colours[counter], line_width=3, muted_alpha=0.2 ) ] ))
	leg_1.append(( pop, [plot_b.scatter(x='Class', y='Mean', source=source.loc[source['Population'] == pop],
		marker=markers[counter], size=15, color=colours[counter], muted_alpha=0.6, fill_color=filling[counter] ) ] ))

label_opts= dict(x=0, y=0, x_units='screen', y_units='screen', text_font_size='14pt')
caption= Label(text=' Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).', **label_opts)
plot_b.add_layout(caption, "below")
plot_b.title.text_font_size = '18pt'

plot_b.xaxis.major_label_overrides = {1: '[0.3-0.5Mb)', 2:'[0.5-1Mb)', 3:'[1-2Mb)', 4:'[2-4Mb)', 5:'[4-8Mb)', 6:'[8-16Mb)' }
plot_b.xaxis.axis_label="ROH length category"
plot_b.xaxis.axis_label_text_font_size = "17pt"
plot_b.xaxis.major_label_text_font_size = "13pt"
plot_b.xaxis.axis_label_text_font= "arial"
plot_b.xaxis.axis_label_text_color= "black"
plot_b.xaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.xaxis.major_tick_line_width= 5

plot_b.yaxis.axis_label="Mean total length of ROH (Mb)"
plot_b.yaxis.axis_label_text_font_size = "17pt"
plot_b.yaxis.major_label_text_font_size = "15pt"
plot_b.yaxis.axis_label_text_font= "arial"
plot_b.yaxis.axis_label_text_color= "black"
plot_b.yaxis.axis_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_label_text_font_style= "bold" # "normal" or "italic"
plot_b.yaxis.major_tick_line_width= 5

#Grid lines
plot_b.xgrid.visible = False
plot_b.xgrid.grid_line_alpha = 0.8
plot_b.xgrid.grid_line_dash = [6, 4]
plot_b.ygrid.visible = False
plot_b.ygrid.grid_line_alpha = 0.8
plot_b.ygrid.grid_line_dash = [6, 4]

#Legend
ncolumn=int((len(Populations)+3)/4)+1
legend1 = Legend(
    items=leg_0[0:ncolumn], location=(0, 30),)

legend2 = Legend(
    items=leg_0[ncolumn:ncolumn*2], location=(0, 30))

legend3 = Legend(
    items=leg_0[ncolumn*2:ncolumn*3], location=(0, 30))

legend4 = Legend(
    items=leg_0[ncolumn*3:], location=(0, 30))

plot_b.add_layout(legend1, 'right')
plot_b.add_layout(legend2, 'right')
plot_b.add_layout(legend3, 'right')
plot_b.add_layout(legend4, 'right')

plot_b.legend.location = "top_right"
plot_b.legend.click_policy="hide"#"mute"
plot_b.legend.label_text_font_size = '8pt'

plot_b.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [
	 ('Population:', '@Population'),
		 ]
	 ))

#######################

# Make a grid
grid= layout([[plot_a],[plot_b]]) #, width=1800, height=700)
show(grid)

# Save plots
print("Saving Figure S21")
export_png(grid, filename=args.output+".png")

# grid.output_backend= "svg"
# export_svgs(grid, filename=args.output+".svg")

exit()

#######################

