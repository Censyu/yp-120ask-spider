#!/bin/bash
loop=0
count=0
rount=1
while(( $loop<40 ))
do
	begin=$[$loop*5000]
	end=$[($loop+1)*5000]
	nohup python yp-spider-batch.py ${begin} ${end} &> log/$loop &
	let "loop++"
	let "count++"
	if(($count>=4))
	then
		let "round++"
		echo "round $round"
		count=0
		sleep 1200
	fi
done

