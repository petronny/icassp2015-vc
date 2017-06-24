#!/bin/sh
matlab=matlab-r2015b
hash=`cat /proc/sys/kernel/random/uuid`
mfile="/tmp/matlab_$hash.m"

cp `dirname $0`/../matlab/straight_features.m $mfile
sed \
	-e "s|STRAIGHT_PATH|$(dirname $0)/../matlab/STRAIGHT|" \
	-e "s|WAVFILE|$1|" \
	-i $mfile
rm -f $target
$matlab -singleCompThread -nosplash -nodisplay -nojvm < $mfile
rm $mfile
