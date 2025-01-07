
This README gives information about how to run the plotting scripts included in this repository.
Scripts were run using Python v3.8.6 (in particular, the library Bokeh v3.1.1) and R v4.4.1.

The repository provides all the tables and additional information to run all the scripts with a few command lines. 
First, please check that you have installed all the Python and R libraries/packages included in the scripts.

```
git clone https://github.com/Schlebusch-lab/Sahel_study.git
cd Sahel_study

# Check that you don't have an error message after using:
python3 scripts/bokeh_Figure_2B.py --help

[Optional for all the scripts]
ls scripts/*.py | while read line; do python3 ${line} --help; done

# In R
library(admixtools)
library(plotly)
library(rworldmap)
library(plotrix)
library(basicPlotteR)

# If you don't have basicPlotteR, you can install it as follows:
remotes::install_github("JosephCrispell/basicPlotteR")

```

# Main Figures #

#### Figure 1 | PCA and PCA-UMAP results ####
```
### Figures 1A-E | PCA results to explore the genetic diversity among studied Fulani population.

DB="Tables/Only-Fulani_DB"
python3 scripts/bokeh_Figure_1A-E.py --output 01-Main_Figures/Figure_1A-E \
 --input_A ${DB}.map.csv --input_B ${DB}.pca.evec -p ${DB}_pca.csv

Figures 1F-G | PCA-UMAP on the basis of Fulani and other Western and Central African populations
python3 scripts/bokeh_Figure_1F-G.py --input Tables/Fulani_PCA-UMAP_table.txt --output 01-Main_Figures/Figure_1F-G
 --pattern_A Tables/Fulani_PCA-UMAP_pattern_A.csv --pattern_B Tables/Fulani_PCA-UMAP_pattern_B.csv


```
### Figure 2 ###
```
Table_A='Tables/Fulani-World_DB'
Table_B='Tables/Fulani_aDNA-Modern_DB'

###  Figures 2A and 2C | PC1 and PC2 for modern Fulani and reference populations and for ancient individuals.

python3 scripts/bokeh_Figure_2A-C.py --input_A ${Table_A}.pca.evec --input_B ${Table_B}.pca.evec \
 --pattern_A ${Table_A}_pca.csv --pattern_B ${Table_B}_grey.csv -o 01-Main_Figures/Figure_2A-C

###  Figure 2B | PC1 and PC3 for modern Fulani and reference populations and for ancient individuals.

python3 scripts/bokeh_Figure_2B.py --input_A ${Table_A}.pca.evec --input_B ${Table_B}.pca.evec \
 --pattern_A ${Table_A}_pca.csv --pattern_B ${Table_B}_grey.csv -o 01-Main_Figures/Figure_2B

###  Figure 2D | ADMIXTURE results at K=6.

Rscript scripts/piechartMap.r "Figure 2D. ADMIXTURE results at K=6" \
 Tables/ADMIXTURE_Fulani_aDNA-Modern_DB.K6.Q.csv 01-Main_Figures/Figure_2D

[Optional: Include the label for each studied population by using the suffix "With_Labels" in the output name.]
Rscript scripts/piechartMap.r "Figure 2D. ADMIXTURE results at K=6" \
 Tables/ADMIXTURE_Fulani_aDNA-Modern_DB.K6.Q.csv 01-Main_Figures/Figure_2D_With_Labels

```
### Figures 4A and S20 | Effective population sizes (Ne) estimated for each Fulani population. ###
```
python3 scripts/bokeh_Figure_4A.py --output "01-Main_Figures/Figure_4A"

```
### Figures 4B and S21 | Categories of ROH length based on the studied populations. ###
```
python3 scripts/bokeh_Figure_S21.py --output "02-Suppl_Figures/Figure_S21" \
 --input_A "Tables/Only-Fulani_DB.ROH_Class_table.txt" \
 --input_B "Tables/Fulani-World_DB.ROH_Class_table.txt"

```

# Supplementary Figures #

### Figure S3 | Distribution of modern and ancient populations included in this study. ###
```
python3 scripts/bokeh_Figure_S3.py --output 02-Suppl_Figures/Figure_S03 \
 --input_A Tables/Fulani-World_DB.map.csv --input_B Tables/Fulani_aDNA-Modern_DB.map.csv

```
### Figure S5 | PCA of Fulani and reference populations. ###
```
DB="Tables/Fulani-World_DB"
python3 scripts/bokeh_Figure_S5.py -i ${DB}.pca.evec -p ${DB}_pca.csv -o 02-Suppl_Figures/Figure_S05

```
### Figure S6 | Geographical distribution and PCA of Fulani and reference populations. ###
```
DB="Tables/Fulani-WGS_DB"
python3 scripts/bokeh_Figure_S6.py --output 02-Suppl_Figures/Figure_S06 \
 --input_A ${DB}.map.csv --input_B ${DB}.pca.evec -p ${DB}_pca.csv

```
### Figure S9A | ADMIXTURE results at K=7 using the projection mode. ###
```
Rscript scripts/piechartMap_Figure_S9A.r "Figure S9A. ADMIXTURE results at K=7" \
 Tables/ADMIXTURE_Fulani-World_DB.K7.Q.csv 02-Suppl_Figures/Figure_S9A

[Optional: Include the label for each population by using the suffix "With_Labels" in the output name.]
Rscript scripts/piechartMap_Figure_S9A.r "Figure S9A. ADMIXTURE results at K=7" \
 Tables/ADMIXTURE_Fulani-World_DB.K7.Q.csv 02-Suppl_Figures/Figure_S9A_With_Labels

```
### Figure S13 | PCA based on modern and ancient individuals. ###
```
DB='Tables/Fulani_aDNA-Modern_DB'
python3 scripts/bokeh_Figure_S13.py -i ${DB}.evec -p ${DB}_pca.csv -o 02-Suppl_Figures/Figure_S13

```
### Figure S14 | ADMIXTURE results at K=6 based on modern and aDNA individuals. ###
```
Rscript scripts/ADMIXTURE_Fulani_aDNA-Modern_DB.K6.r

[Optional: Save plot in PNG format.]
Fig='02-Suppl_Figures/Figure_S14'; pdftoppm ${Fig}.pdf ${Fig} -png -r 300

```
### Figure S15 | ADMIXTURE results at K=8 based on modern and aDNA individuals. ###
```
Rscript scripts/ADMIXTURE_Fulani_aDNA-Modern_DB.K8.r

[Optional: Save plot in PNG format.]
Fig='02-Suppl_Figures/Figure_S15'; pdftoppm ${Fig}.pdf ${Fig} -png -r 300

```
### Figure S16 | Admixture graph for Fulani from Assaba (Mauritania) and reference populations. ###
```
# In R
library(admixtools)
library(plotly)

pop <- "Mauritania_Fulani_Assaba"
winner_graph <- read.table(paste0("Tables/Admixture_graphs/",pop,"_edges.tsv"), sep="\t", header=T)

# plotly_graph(winner_graph)
pdf("02-Suppl_Figures/Figure_S16.pdf", height=16, width=14)
plot_graph(winner_graph, textsize =5)
dev.off()

# This is the figure obtained before bootstrapping using the qpgraph_resample_snps function as follows.
# fits = qpgraph_resample_snps(f2_blocks, winner_graph, boot = 1000)
# p <- fits %>% summarize_fits() %>% plotly_graph(print_highlow = TRUE)
# htmlwidgets::saveWidget(as_widget(p), "02-Suppl_Figures/Figure_S16.html")

```
### Figure S17 | Admixture graph for Fulani from Banfora (Burkina Faso) and reference populations. ###
```
# In R
library(admixtools)
library(plotly)

pop <- "BurkinaFaso_Fulani_Banfora"
winner_graph <- read.table(paste0("Tables/Admixture_graphs/",pop,"_edges.tsv"), sep="\t", header=T)

# plotly_graph(winner_graph)
pdf("02-Suppl_Figures/Figure_S17.pdf", height=16, width=14)
plot_graph(winner_graph, textsize =5)
dev.off()

# This is the figure obtained before bootstrapping using the qpgraph_resample_snps function as follows.
# fits = qpgraph_resample_snps(f2_blocks, winner_graph, boot = 1000)
# p <- fits %>% summarize_fits() %>% plotly_graph(print_highlow = TRUE)
# htmlwidgets::saveWidget(as_widget(p), "02-Suppl_Figures/Figure_S17.html")

```
### Figure S18 | Admixture graph for Fulani from Abalak (Niger) and reference populations. ###
```
# In R
library(admixtools)
library(plotly)

pop <- "Niger_Fulani_Abalak"
winner_graph <- read.table(paste0("Tables/Admixture_graphs/",pop,"_edges.tsv"), sep="\t", header=T)

# plotly_graph(winner_graph)
pdf("02-Suppl_Figures/Figure_S18.pdf", height=16, width=14)
plot_graph(winner_graph, textsize =5)
dev.off()

# This is the figure obtained before bootstrapping using the qpgraph_resample_snps function as follows.
# fits = qpgraph_resample_snps(f2_blocks, winner_graph, boot = 1000)
# p <- fits %>% summarize_fits() %>% plotly_graph(print_highlow = TRUE)
# htmlwidgets::saveWidget(as_widget(p), "02-Suppl_Figures/Figure_S18.html")

```
### Figure S19 | Admixture graph for Fulani from Linia (Chad) and reference populations. ###
```
# In R
library(admixtools)
library(plotly)

pop <- "Chad_Fulani_Linia"
winner_graph <- read.table(paste0("Tables/Admixture_graphs/",pop,"_edges.tsv"), sep="\t", header=T)

# plotly_graph(winner_graph)
pdf("02-Suppl_Figures/Figure_S19.pdf", height=16, width=14)
plot_graph(winner_graph, textsize =5)
dev.off()

# This is the figure obtained before bootstrapping using the qpgraph_resample_snps function as follows.
# fits = qpgraph_resample_snps(f2_blocks, winner_graph, boot = 1000)
# p <- fits %>% summarize_fits() %>% plotly_graph(print_highlow = TRUE)
# htmlwidgets::saveWidget(as_widget(p), "02-Suppl_Figures/Figure_S19.html")

```
### Figure S21 | Categories of ROH length on the basis of the studied populations. ###
```
python3 scripts/bokeh_Figure_S21.py --output "02-Suppl_Figures/Figure_S21"
 --input_A "Tables/Only-Fulani_DB.ROH_Class_table.txt" \
 --input_B "Tables/Fulani-World_DB.ROH_Class_table.txt"

```
### Figure S22 | Violin plots for ROH parameters estimated for each studied population. ###
```
# The same script can plot the following figures
# Figure S22A | Total sum of short and long ROH for each studied population.
# Figure S22B | Total sum of long ROH for each studied population.
# Figure S23A | Genomic inbreeding coefficients for each studied population.
# Figure S23B | Total length of ROH for each studied population.

python3 scripts/ROH_violin_plots.py 

```

#### Contact person of this repository:
##### Cesar Fortes-Lima (Github account: https://github.com/cesarforteslima). Emails: cfortes2@jh.edu; cesar.fortes-lima@ebc.uu.se
More scripts, tables and figures are available upon request.

