# Main Figure S9A
# __author__= 'Cesar Fortes-Lima'

library(rworldmap)
library(plotrix)
# remotes::install_github("JosephCrispell/basicPlotteR")
library(basicPlotteR)

args <- commandArgs(trailingOnly= T)
options(warn=-1)

# Usage:
# Rscript scripts/piechartMap_Figure_S9A.r "Figure S9A. ADMIXTURE results at K=7" Tables/ADMIXTURE_Fulani-World_DB.K7.Q.csv 02-Suppl_Figures/Figure_S09A
# Rscript scripts/piechartMap_Figure_S9A.r "Figure S9A. ADMIXTURE results at K=7" Tables/ADMIXTURE_Fulani-World_DB.K7.Q.csv 02-Suppl_Figures/Figure_S09A_With_Labels
# Outputs witht the sufix "With_Labels" will take more time to create. Please be patient.

Figure= args[1] # Figure header

inputfile.name = args[2]
inputfile <- read.csv(inputfile.name, header= F, as.is= T)
inputfile <- as.data.frame(inputfile)

outputfile.name= args[3]

if (T==grepl("With_Labels", outputfile.name, fixed=TRUE)) {
  print.labels = T
} else {
  print.labels = F
}

# Select the colors for the piecharts 
colours= c("green","black","violet","brown","green4","royalblue","purple4")

plot.piechart <- function(admixData, labels) {
  #plots map and axes
  worldmap <- getMap(resolution = "high")
  plot(worldmap, xlim= c(min(admixData[,3]), max(admixData[,3])), ylim= c(min(admixData[,4]-2), max(admixData[,4])), col="floralwhite")
  box(which="plot")
  axis(1)
  axis(2)
  
  chart.data <- admixData[5:11]
  for (x in 1:nrow(admixData)) {
    floating.pie(admixData[x,3], admixData[x,4], unlist(chart.data[x,]),  lwd= 1, border= "gray30",
		radius= (admixData[x,2])/20, col= colours)
  }
  #function to put labels in the map
  if (labels) {
    for (x in 1:nrow(admixData)) {
		addTextLabels(x = admixData$V3, y = admixData$V4, labels= admixData$V1, cex.label= 0.6, cex.pt= 1.8, col.label= "gray10",
		col.line= "gray", lwd= 1, lty= 3, keepLabelsInside= F)#, avoidFactor= 2, col.background=NULL, border= NA, avoidPoints= T)
      #text(admixData[x,3], admixData[x,4], labels=admixData[x,1], cex= 0.9, pos = 3, offset = 1)
    }
  }

mtext(Figure, side=3, adj=0, line=2, col="black", font=2, cex=1.5)
mtext("Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).", side=3, adj=0, line=0, col="black", cex=1.2)

}

pdf(file = paste(outputfile.name,".pdf", sep=""), title= outputfile.name, width= 10, height= 10)
plot.piechart(inputfile,print.labels)
dev.off()

png(filename = paste(outputfile.name,".png", sep=""), width= 800, height= 800)
plot.piechart(inputfile,print.labels)
dev.off()

#####################

