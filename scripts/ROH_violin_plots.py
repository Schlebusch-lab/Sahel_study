#!/usr/bin/python
"""
Plotting script for Suppl Figures S22 and S23.
"""
__author__ = 'Cesar Fortes-Lima'

# Usage:
# python3 scripts/ROH_violin_plots.py 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

table_name= "Tables/Fulani-World_ROH.csv"
table = pd.read_csv(table_name, sep=',')
df = pd.DataFrame(table)

palette=('#66AEBF','#3B9AB2','#57A7BA','#49A0B6','#74B5C3','#8CBAA9','#C2C460','#A7BF85','#E9C825','#DDC93C','#E5BA11','#E7C11B','#E58300','#E2A600','#E2B407','#E58300','#F21A00','#EE3D00','#004529','#ADDD8E','#78C679','#238443','#41AB5D','#ADDD8E','#238443','#006837','#004529','#004529','#ADDD8E','#006837','#78C679','#78C679','#41AB5D','#ADDD8E','#238443','#006837','#41AB5D','#543005','#8C510A','#BF812D','#DFC27D','#543005','#8C510A','#BF812D','#DFC27D','#543005','#BF812D','#DFC27D','#543005','#DFC27D','#8C510A','tan','tan','tan','tan','skyblue','skyblue','skyblue','skyblue','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray','darkslategray')

##########

plt.figure(figsize=(12,20))
output= "02-Suppl_Figures/Figure_S22A"
plt.title("Figure S22A | Total sum of short ROH for each studied population", loc="left", fontsize=16)
plt.suptitle("Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).", fontsize=12)
ax = sns.violinplot(data=df, hue='Population', x='Sum_short_ROH', y='Population', cut=0, density_norm="width", palette=palette, legend=False)
ax.set(xlabel="Total sum of short ROH (<1.5Mb)", ylabel = "Population")
ax.tick_params(axis='y', labelsize=12)
#plt.show()
plt.savefig(output+".pdf")
print("Plotting Figure S22A")

##########

plt.figure(figsize=(12,20))
output= "02-Suppl_Figures/Figure_S22B"
plt.title("Figure S22B | Total sum of long ROH for each studied population", loc="left", fontsize=16)
plt.suptitle("Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).", fontsize=12)
ax = sns.violinplot(data=df, hue='Population', x='Sum_long_ROH', y='Population', cut=0, density_norm="width", palette=palette, legend=False)
ax.set(xlabel="Total sum of long ROH (>1.5Mb)", ylabel = "Population")
ax.tick_params(axis='y', labelsize=12)
#plt.show()
plt.savefig(output+".pdf")
print("Plotting Figure S22B")

##########

plt.figure(figsize=(12,20))
output= "02-Suppl_Figures/Figure_S23A"
plt.title("Figure S23A | Genomic inbreeding coefficients for each studied population", loc="left", fontsize=16)
plt.suptitle("Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).", fontsize=12)
ax = sns.violinplot(data=df, hue='Population', x='F_ROH', y='Population', cut=0, density_norm="width", palette=palette, legend=False)
ax.set(xlabel="FROH (inbreeding coefficient)", ylabel = "Population")
ax.tick_params(axis='y', labelsize=12)
#plt.show()
plt.savefig(output+".pdf")
print("Plotting Figure S23A")

##########

plt.figure(figsize=(12,20))
output= "02-Suppl_Figures/Figure_S23B"
plt.title("Figure S23B | Total length of ROH for each studied population", loc="left", fontsize=16)
plt.suptitle("Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).", fontsize=12)
ax = sns.violinplot(data=df, hue='Population', x='Total_length_ROH', y='Population', cut=0, density_norm="width", palette=palette, legend=False)
ax.set(xlabel="Total length of ROH (>1.5Mb)", ylabel = "Population")
ax.tick_params(axis='y', labelsize=12)
#plt.show()
plt.savefig(output+".pdf")
print("Plotting Figure S23B")

##########

exit()
