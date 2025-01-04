
## Main Figure 1

###  Figure 1A | Map only for Fulani populations.
python3 ${Folder}/scripts/bokeh_interactive_map.py -i Patterns/Only-BSP_Groups_imputation_df.csv -o ${Folder}/Fig_3/Fig_3map -w 1000 -t "" -a ""

###  Figure 1F | PCA plot to explore the genetic diversity among studied Fulani populations.
Folder="Main_Figures"; DB="Only-African_Groups"
python3 ${Folder}/scripts/bokeh_interactive_map.py -i 01-Maps/Map_${DB}_df.csv -o ${Folder}/Fig_1/Fig_1a -w 2100 -t "" -a ""


## Main Figure 2
Table_A='Tables/Fulani-World_DB'
Table_C='Tables/Fulani_aDNA-Modern_DB'

###  Figure 2A and 2C | PC1 and PC2 for modern Fulani and reference populations and for ancient individuals.
python3 scripts/bokeh_Figure_2A-2C.py --input_A ${Table_A}.pca.evec --input_C ${Table_C}.pca.evec \
 --pattern_A ${Table_A}_pca.csv --pattern_C ${Table_C}_grey.csv -o 01-Main_Figures/Figure_2A-C

###  Figure 2B | PC1 and PC3 for modern Fulani and reference populations and for ancient individuals.
python3 scripts/bokeh_Figure_2B.py --input_A ${Table_A}.pca.evec --input_C ${Table_C}.pca.evec \
 --pattern_A ${Table_A}_pca.csv --pattern_C ${Table_C}_grey.csv -o 01-Main_Figures/Figure_2B

###  Figure 2D | ADMIXTURE results at K=6
Rscript scripts/piechartMap.r "Figure 2D. ADMIXTURE results at K=6" Tables/ADMIXTURE_Fulani_aDNA-Modern_DB.K6.Q.csv 01-Main_Figures/Figure_2D

[Optional: Include label for each population by using the sufix "With_Labels" in the output name.]
Rscript scripts/piechartMap.r "Figure 2D. ADMIXTURE results at K=6" Tables/ADMIXTURE_Fulani_aDNA-Modern_DB.K6.Q.csv 01-Main_Figures/Figure_2D_With_Labels



##################  Supplementary Figures  ##################  

## Suppl Figure S3
python3 scripts/bokeh_Figure_S3.py --input_A Tables/Fulani-World_DB.csv --input_B Tables/Fulani_aDNA-Modern_DB.csv --output Suppl_Figures/Figure_S3
#
#

## Suppl Figure S6
### Figure S6A
python3 ${Folder}/scripts/bokeh_interactive_map.py -i 01-Maps/Map_${DB}_df.csv -o ${Folder}/Fig_1/Fig_1a -w 2100 -t "" -a ""

## Suppl Figure S9A
Rscript scripts/piechartMap_Figure_S9A.r "Figure S9A. ADMIXTURE results at K=7" Tables/ADMIXTURE_Fulani-World_DB.K7.Q.csv 02-Suppl_Figures/Figure_S9A

[Optional: Include label for each population by using the sufix "With_Labels" in the output name.]
Rscript scripts/piechartMap_Figure_S9A.r "Figure S9A. ADMIXTURE results at K=7" Tables/ADMIXTURE_Fulani-World_DB.K7.Q.csv 02-Suppl_Figures/Figure_S9A_With_Labels

## Suppl Figure S13
DB='Tables/Fulani_aDNA-Modern_DB'
python3 scripts/bokeh_Figure_S13.py -i ${DB}.evec -p ${DB}_pca.csv -o 02-Suppl_Figures/Figure_S13

## Suppl Figure S14
Rscript scripts/ADMIXTURE_Fulani_aDNA-Modern_DB.K6.r
Fig='02-Suppl_Figures/Figure_S14'; pdftoppm ${Fig}.pdf ${Fig} -png -r 300

## Suppl Figure S15
Rscript scripts/ADMIXTURE_Fulani_aDNA-Modern_DB.K8.r
Fig='02-Suppl_Figures/Figure_S15'; pdftoppm ${Fig}.pdf ${Fig} -png -r 300


