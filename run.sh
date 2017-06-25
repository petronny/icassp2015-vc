#!/bin/sh
settings(){
	#cores=`lscpu | grep "CPU(s):" | awk '{print $2}'`
	cores=32
	test_suffix='1'
	steps=(
		cleanup
		fetch_data
		straight_features
		sp2mcep
		dtw
		generate_datasets
		concat_features
		DNN
		DNN_dyn
		DBLSTM
		DBLSTM_dyn
		test_models
	)
}

cleanup(){
	echo "Cleaning up"
	rm -rf models tmp
	mkdir -p data tmp models
}

fetch_data(){
	prefix="http://festvox.org/cmu_arctic/cmu_arctic/packed"
	for i in cmu_us_awb_arctic-0.95-release.tar.bz2 cmu_us_slt_arctic-0.95-release.tar.bz2
	do
		[ ! -f data/$i ] && echo Downloading $i && wget -O data/$i "$prefix/$i"
		echo Extracting $i
		tar xf data/$i -I pbzip2 -C tmp/
	done
	rm -f tmp/wavlist.txt
	for i in tmp/cmu_us_awb_arctic/wav/*.wav
	do
		if [ -f ${i/awb/slt} ]
		then
			echo $i >> tmp/wavlist.txt
		fi
	done
}

straight_features(){
	echo "Extracting STRAIGHT features"
	cat tmp/wavlist.txt|$parallel sh tools/features/straight-features.sh >/dev/null
	cat tmp/wavlist.txt|sed 's/awb/slt/g'|$parallel sh tools/features/straight-features.sh >/dev/null
}

sp2mcep(){
	echo "Calucating MCEP"
	cat tmp/wavlist.txt|sed 's/wav$/sp.csv/g'|$parallel sh tools/features/sp2mcep.sh
	cat tmp/wavlist.txt|sed -e 's/wav$/sp.csv/g' -e 's/awb/slt/g'|$parallel sh tools/features/sp2mcep.sh
}

dtw(){
	echo "Doing Dynamic Time Warping"
	rm -f tmp/problemlist.txt
	cat tmp/wavlist.txt|sed 's/wav$/mcep.csv/g'|$parallel sh tools/features/dtw.sh >> tmp/problemlist.txt
	sed 's/mcep\.csv$/wav/g' -i tmp/problemlist.txt
}

generate_datasets(){
	echo "Generating datasets"
	rm -f tmp/{train,test}list.txt
	count=0
	for i in `cat tmp/wavlist.txt`
	do
		[ `grep -c $i tmp/problemlist.txt` -ge 1 ] && continue
		[ $count -eq $test_suffix ] && echo $i >> tmp/testlist.txt || echo $i >> tmp/trainlist.txt
		count=$((($count+1)%5))
	done
}

concat_features(){
	echo "Concatenating features"
	rm tmp/*.{npy,pkl}
	sed 's/wav$/mcep.csv/g' tmp/trainlist.txt | python keras/concat_features.py tmp/train_source
	sed 's/wav$/mcep.csv/g' tmp/testlist.txt | python keras/concat_features.py tmp/test_source
	sed -e 's/awb/slt/g' -e 's/wav$/mcep.csv/g' tmp/trainlist.txt | python keras/concat_features.py tmp/train_target
	sed -e 's/awb/slt/g' -e 's/wav$/mcep.csv/g' tmp/testlist.txt | python keras/concat_features.py tmp/test_target
	sed 's/wav$/mcep.dtw.csv/g' tmp/trainlist.txt | python keras/concat_features.py tmp/train_source.dtw
	sed 's/wav$/mcep.dtw.csv/g' tmp/testlist.txt | python keras/concat_features.py tmp/test_source.dtw
	sed -e 's/awb/slt/g' -e 's/wav$/mcep.dtw.csv/g' tmp/trainlist.txt | python keras/concat_features.py tmp/train_target.dtw
	sed -e 's/awb/slt/g' -e 's/wav$/mcep.dtw.csv/g' tmp/testlist.txt | python keras/concat_features.py tmp/test_target.dtw
}

DNN(){
	echo "Training the DNN model"
	python keras/DNN.py 0
}

DNN_dyn(){
	echo "Training the DNN model with dynamic features"
	python keras/DNN_dyn.py 0
}

DBLSTM(){
	echo "Training the DBLSTM model"
	python keras/DBLSTM.py 0
}

DBLSTM_dyn(){
	echo "Training the DBLSTM model with dynamic features"
	python keras/DBLSTM_dyn.py 0
}

test_models(){
	echo "Testing models"
	python keras/test.py 0
}

print_help(){
	echo "Usage:"
	echo "	$0 <#step>"
	echo "	$0 <#begin_step> <#end_step>"
	echo
	echo -e \#\\tstep
	for step in `seq 0 $num_of_steps`
	do
		echo -e $step\\t${steps[$step]}
	done
}

main(){
	settings
	parallel="xargs --max-args=1 --max-procs=$cores"
	num_of_steps=$((${#steps[@]}-1))
	print_help

	[ -n "$1" ] && beginstep=$1 || exit
	[ -n "$2" ] && endstep=$2 || endstep=$1

	echo
	echo "Running from step $beginstep to step $endstep"

	for step in `seq $beginstep $endstep`
	do
		${steps[$step]}
	done
}
main $@
