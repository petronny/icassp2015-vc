#!/bin/sh
target=`echo $1| sed -e 's/\.sp.csv$/.mcep.csv/'`
mcep_order=49

x2x \
	+af $1 |
mcep \
	-a 0.55 \
	-m $mcep_order \
	-l 2048 \
	-e 1e-8 \
	-f 1e-8 \
	-q 3 |
x2x \
	+fa$(($mcep_order+1)) \
	> $target
