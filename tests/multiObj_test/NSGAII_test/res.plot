set term png size 1024, 768
set output "figure.png"

set ticslevel 0

set xrange [-2:20]
set xtics 2
set yrange [-5:20]

set style line 1 pt 1
set style line 2 pt 1

set multiplot

plot "pyga.res" using 1:2 with points
replot "pyga_pareto.res" using 1:2 with points
