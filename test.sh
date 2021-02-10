echo "every Tuesday,Wednesday,Tuesday at 1200,1100 run /bin/date" > "conf.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: every Tuesday,Wednesday,Tuesday at 1200,1100 run /bin/date" ]
then
    echo "Test case: Duplicate days - Passed"
else
    echo "Test case: Duplicate days - Failed"
fi

echo "on tuesday at 1300 run /bin/echo hello world" > "conf.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: on tuesday at 1300 run /bin/echo hello world" ]
then
    echo "Test case: Incorrect case - Passed"
else
    echo "Test case: Incorrect case - Failed"
fi

echo "every Mon at 1430,0900 run /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: every Mon at 1430,0900 run /bin/echo hello world" ]
then
    echo "Test case: Incorrect day name - Passed"
else
    echo "Test case: Incorrect day name - Failed"
fi

echo "Every Tuesday at 0500 run /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: Every Tuesday at 0500 run /bin/echo hello world" ]
then
    echo "Test case: Incorrect keyword - Passed"
else
    echo "Test case:  Incorrect keyword - Failed"
fi

echo "ON Monday,Wednesday at 0930 run /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: ON Monday,Wednesday at 0930 run /bin/echo hello world" ]
then
    echo "Test case: Incorrect keyword - Passed"
else
    echo "Test case: Incorrect keyword - Failed"
fi

echo "aT 2359 run run /bin/cp  /tmp/a /tmp/b" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: aT 2359 run run /bin/cp  /tmp/a /tmp/b" ]
then
    echo "Test case: Incorrect keyword - Passed"
else
    echo "Test case: Incorrect keyword - Failed"
fi

echo "at 3630 run /bin/cp  /tmp/a /tmp/b" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: at 3630 run /bin/cp  /tmp/a /tmp/b" ]
then
    echo "Test case: Incorrect time - Passed"
else
    echo "Test case: Incorrect time - Failed"
fi

echo "every Thursday at 0960 run /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: every Thursday at 0960 run /bin/echo hello world" ]
then
    echo "Test case: Incorrect time - Passed"
else
    echo "Test case: Incorrect time - Failed"
fi

echo "on Saturday at 12000 run /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: on Saturday at 12000 run /bin/echo hello world" ]
then
    echo "Test case: Incorrect time - Passed"
else
    echo "Test case: Incorrect time - Failed"
fi

echo "on Monday,Tuesday at 1000,1200,1000 run /bin/echo Hello World!" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: on Monday,Tuesday at 1000,1200,1000 run /bin/echo Hello World!" ]
then
    echo "Test case: Duplicate times - Passed"
else
    echo "Test case: Duplicate times - Failed"
fi

echo "every Friday at 1545 run /bin/echo hello world" > "~/runner.conf"
echo "on Thursday,Friday at 1545,2200 run /bin/echo hello world" >> "conf.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: on Thursday,Friday at 1545,2200 run /bin/echo hello world" ]
then
    echo "Test case: Duplicate times - Passed"
else
    echo "Test case: Duplicate times - Failed"
fi

echo "every Wednesday,Sunday at 1800 /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: every Wednesday,Sunday at 1800 /bin/echo hello world" ]
then
    echo "Test case: No 'run' keyword - Passed"
else
    echo "Test case: No 'run' keyword - Failed"
fi

echo "on at Sunday 1900 run /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: on at Sunday 1900 run /bin/echo hello world" ]
then
    echo "Test case: Invalid syntax - Passed"
else
    echo "Test case: Invalid syntax - Failed"
fi

echo "every Thursday,Tuesday at 2130,1345 run" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: every Thursday,Tuesday at 2130,1345 run" ]
then
    echo "Test case: No program path - Passed"
else
    echo "Test case: No program path - Failed"
fi

echo "on Sunday at twothirty run /bin/echo hello world" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: on Sunday at twothirty run /bin/echo hello world" ]
then
    echo "Test case: Invalid time - Passed"
else
    echo "Test case: Invalid time - Failed"
fi

echo "every Thursday at 123 run run /bin/date" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: every Thursday at 123 run run /bin/date" ]
then
    echo "Test case: Invalid time - Passed"
else
    echo "Test case: Invalid time - Failed"
fi

echo "on Tuesday at 12-0 run /bin/date" > "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "error in configuration: on Tuesday at 12-0 run /bin/date" ]
then
    echo "Test case: Invalid time - Passed"
else
    echo "Test case: Invalid time - Failed"
fi

> "~/runner.conf"
output=$(python3 runner.py 2>&1)
if [ "$output" == "configuration file empty" ]
then
    echo "Test case: Empty configuration file - Passed"
else
    echo "Test case: Empty configuration file - Failed"
fi