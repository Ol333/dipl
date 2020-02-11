#!/usr/bin/gnuplot
set grid
set term postscript color enhanced eps
set out "./out/graph.eps"
#set yrange [0:5]
plot "./out/kin.txt" w l lc 6 title "Kinetic solution", "./out/ana.txt" w l lc 7 title "Analytic Solution"
