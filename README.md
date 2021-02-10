# cron-program


The program reads in a configuration file that specifies what programs are to be run and when. You are able to specify that a given program is run periodically at particular times, for example every Tuesday at 1pm, run a certain script. Alternatively you could specify that a program be run at 8am, 12noon, 2pm and 4pm everyday.

The system consists of two programs:

1. The program (runner.py) which runs in the background, reading the configuration file which specifies which programs (with parameters) it should run and when they should be started.
2. The second command (runstatus.py) is designed to get the current status from runner.py and send it to the standard output.
