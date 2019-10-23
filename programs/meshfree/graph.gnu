#!/usr/bin/gnuplot
set grid
set term postscript color enhanced eps
set out "./out/graph.eps"
#set yrange [0:5]
plot "./out/monteCarlo.txt" w l title "Monte Carlo", "./out/analyticSolution.txt" w l title "Analytic Solution", "./out/diffScheme.txt" w l lc 7 title "Numeric Solution"
