set term png size 1024, 768
set output "figure.png"

plot "pyga.res" using 1:2 with points title "final population", \
     "pyga_pareto.res" using 1:2 with points title "pareto front", \
     "pyga_init.res" using 1:2 with points title "init population"
