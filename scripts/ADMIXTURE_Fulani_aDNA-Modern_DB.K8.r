# Figure S15 | ADMIXTURE results at K=8 on the basis modern and aDNA individuals
# __author__= 'Cesar Fortes-Lima'

############################# define the sector function to draw sector ######################################
sector <- function (x0=0, y0=0, angle1, angle2, radius1, radius2, col, angleinc = 0.03)
{
if (angle1 > angle2) {
temp <- angle1
angle1 <- angle2
angle2 <- temp
}
if (radius1 > radius2) {
temp <- radius1
radius1 <- radius2
radius2 <- temp
}
###########use 4 points polygon to draw a sector########################
angles <- seq(angle1, angle2, by = angleinc)
angles[length(angles)] <- angle2
angles <- angles*(pi/180)
xpos <- c(cos(angles) * radius1, cos(rev(angles)) * radius2) + x0
ypos <- c(sin(angles) * radius1, sin(rev(angles)) * radius2) + y0
polygon(xpos, ypos, col = col, border = col)
}

##############################################################################################################
#args <- commandArgs(trailingOnly=T)
file <- "Tables/ADMIXTURE_Fulani_aDNA-Modern_DB.K8.ancestry"
out <- "02-Suppl_Figures/Figure_S15.pdf"
rmin <- 2
rmax <- 1.85*rmin
amin <- -268
amax <- 91
prgap <- 0.2
col <- c('green','ForestGreen','sienna','grey25','purple2','dodgerblue','grey75','violet','')
indcol <- 1
popcol <- 2
Kstart <- 3
Knum <- 1
pdf(out, 45, 45)
par('oma'=c(10,10,10,10))
par('mar'=c(20, 20, 20, 20))
par('xpd'=TRUE)
plot(0, 0, xlim=c(-rmax, rmax), ylim=c(-rmax, rmax), axes=F, ann=F, type='n')
rstart <- rmin
rlen <- (rmax-rmin)*(1-prgap)/Knum            ####### set the length unit
data <- read.table(file)
popsize <- table(data[,popcol])
npop <- length(popsize)
angelperpop <- (amax - amin)/npop
angelperInd <- angelperpop/popsize
angpre <- amin
############################# draw sectors ##################################################################
for ( i in 1:nrow(data) ){                  ################ for each individual
ang1 <- angpre
ang2 <- ang1 + angelperInd[as.character(data[i,popcol])]
rpre <- rstart
for ( j in Kstart:ncol(data) ){                  ################ for each K
rpost <- rpre + rlen*data[i,j]
sector(angle1=ang1, angle2=ang2, radius1=rpre, radius2=rpost, col=col[j-Kstart+1])   ###### draw sector for each K of each individual
rpre <- rpost}
angpre <- ang2
}
rstart <- rstart + (rmax-rmin)/Knum
lstart <- rmin
lend <- rmax - prgap*(rmax-rmin)/Knum

#############get pop_number angles #################
angles <- seq(amin, amax, length=npop+1)

######################## draw lines for each pop #################################
for ( tmp in angles ){px <- c(lstart*cos(tmp*pi/180), lend*cos(tmp*pi/180))
py <- c(lstart*sin(tmp*pi/180), lend*sin(tmp*pi/180))
lines(px, py, col='black', cex=0.5)}

########################## write all population name #############################
unique <- as.character(unique(data[,popcol]))
npop <- length(unique)
angelperpop <- (amax - amin)/npop
angpre <- amin
for ( i in 1:npop ){
ang <- angpre + angelperpop/2
xx <- lend*cos(ang*pi/180)
yy <- lend*sin(ang*pi/180)
text = unique[i];
cex_no = 220/npop
if(cex_no>10){cex_no=10}
if(cex_no<2.5){cex_no=2.5}
if ( ang < -90 ){text(xx, yy, text, srt=180+ang, adj=c(1.1, 0.5), cex=cex_no, font=2, col=colors()[490])}
else {text(xx, yy, text, srt=ang, adj=c(-0.1, 0.5), cex=cex_no, font=2, col=colors()[490])
}
angpre <- angpre + angelperpop
}

# Add text
mtext("Figure S15. ADMIXTURE results at K=8 on the basis modern and aDNA individuals", side=3, adj=1, line=22, col="black", font=2, cex=3.3)
mtext("Figure presented in Fortes-Lima et al. 2025 AJHG (Copyright 2025).", side=3, adj=1, line=18, col="black", cex=3.3)

dev.off()
