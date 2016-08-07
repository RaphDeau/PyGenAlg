set term png size 1024, 768
set output "figure.png"


splot "pyga.res" using 1:2:3 with points title "final population", \
      "pyga_init.res" using 1:2:3 with points title "init population", \
      "pyga_pareto.res" using 1:2:3 with points title "pareto front"
