#!/bin/bash

echo Stage 1 tests
echo =============
while true
do
	read cline
	echo '==>'$cline
	if [ "$cline" == "END" ]
	then
		echo finished first tests
		break
	fi
	echo "$cline" >runner.conf
	python3 runner.py &
	sleep 2
	python3 runstatus.py
	kill `cat runner.pid`
done <<EOF
on Monday at 2231 run /what/echo Hello 
every Tuesday,Wednesday at 1000,1100 run /bin/echo hello world
at 1300 run /bin/date
every tuesday at 1100 run /bin/date
on Tuesday at 1100 /bin/date
on Tuesday at 11-0 /bin/date
END
EOF

echo Stage 2 test
echo ============
python3 -c 'import time;print(time.strftime("on %A at %H%M run /bin/echo Hello World!\n",time.localtime(int(time.time())+70)),end="")' >~/.runner.conf
echo "===> " `cat runner.conf`
python3 runner.py &
sleep 2
python3 runstatus.py
sleep 120
kill `cat runner.pid`

