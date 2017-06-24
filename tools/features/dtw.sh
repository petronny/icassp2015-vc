#!/bin/sh
target=${1%csv}dtw.csv
hash=`cat /proc/sys/kernel/random/uuid`
mcep_order=49
x2x +af $1 > /tmp/sptk_${hash}_source.sp
x2x +af ${1/awb/slt} > /tmp/sptk_${hash}_target.sp
dtw \
	-m $mcep_order \
	-v /tmp/sptk_${hash}.dtw.path \
	/tmp/sptk_${hash}_target.sp \
	/tmp/sptk_${hash}_source.sp \
	2>/dev/null |
x2x \
	+fa$((2*$mcep_order+2)) \
	> /tmp/sptk_${hash}_source.dtw
[ `du /tmp/sptk_${hash}_source.dtw|cut -f1` -eq 0 ] && echo $1 && rm /tmp/sptk_$hash* && exit
cut -f 1-$(($mcep_order+1)) /tmp/sptk_${hash}_source.dtw > $target
cut -f $(($mcep_order+2))-$((2*$mcep_order+2)) /tmp/sptk_${hash}_source.dtw > ${target/awb/slt}
x2x \
	+ia2 /tmp/sptk_${hash}.dtw.path |
cut -f1 > ${target%csv}path.csv
x2x \
	+ia2 /tmp/sptk_${hash}.dtw.path |
cut -f2 > $(echo ${target%csv}path.csv|sed 's/awb/slt/')

rm /tmp/sptk_$hash*
