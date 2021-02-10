#!/usr/bin/env python3
# -*- coding: ascii -*-

import sys, os, datetime, signal
import time as Time

class Records:
    def __init__(self, keyword, day, time, program_path, parameters):
        self.keyword = keyword
        self.day = day
        self.time = time
        self.program_path = program_path
        self.parameters = parameters
        self.ran = False
        self.errored = False
        self.datetime = 0

days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
global result_list
result_list = []

pid = os.getpid()                             # Get PID and write it to file - runner.pid
try:
    file = open("runner.pid", 'w')
    file.write(str(pid))
    file.close()
except FileNotFoundError:
    sys.stderr.write("file runner.pid not found\n")
    sys.exit()

try:
    file = open("runner.status")              # Checking if file exists, if yes - do nothing, if not - create file
except FileNotFoundError:
    file = open("runner.status", "w")
    file.close()


try:
    file = open("runner.conf")
    if os.path.getsize("runner.conf") == 0:   # Checking if configuration file is empty
        sys.stderr.write("configuration file empty\n")
        sys.exit()
    global lines
    lines = file.readlines()

    listofwords = []                          # Splitting the configuration file by whitespaces and commas
    for line in lines:
        line = line.strip("\n")
        line = line.split(" ")
        words = []
        for word in line:
            if word == '':
                pass
            else:
                word = word.split(",")
                words.append(word)
        listofwords.append(words)

    file.close()
except FileNotFoundError:
    sys.stderr.write("configuration file not found\n")    # Checking if file exists
    sys.exit()


for words in listofwords:                    # Getting rid of whitespaces
    for small_list in words:
        for elem in small_list:
            if elem == '':
                words.remove(small_list)

run_at_list = []
line_number = 0
for instructionLine in listofwords:
    innerlist = []
    if instructionLine[0][0] == 'at':              # Parsing 'at' records
        if instructionLine[2][0] != 'run':
            sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
            sys.exit()
        for time in instructionLine[1]:             # Checking for valid times
            if instructionLine[3].count(time) > 1:                               # Checking for duplicate times
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
            if time.isdigit() == False:                                          # Checking for numeric values
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")   
                sys.exit()   
            if len(time) != 4:                                                   # Checking for correct length
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")   
                sys.exit()
            hour = int(time[:2])
            minute = int(time[2:])
            if hour < 0 or hour > 23:                                            # Checking for correct range
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
            if minute < 0 or minute > 59:
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
        innerlist.append('at')
        j = 0                                         # If record is valid - append to list, each program which is to be run
        while j < len(instructionLine[1]):
            innerlist.append(instructionLine[1][j])
            j += 1
        i = 3
        while i < len(instructionLine):
            innerlist.append(instructionLine[i])
            i += 1
        ls = []
        for item in innerlist:
            ls.append(item)
        for record in run_at_list:
            if record[1] == ls[1] and record[2] == ls[2]:                 # Checking for multiple programs running at the same time
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
        run_at_list.append(ls)
        while len(innerlist) != 1:
            elem = innerlist[1]
            innerlist.remove(elem)
        j += 1
 
    elif instructionLine[0][0] == 'on' or instructionLine[0][0] == 'every':         # Parsing 'on' and 'every' records
        if len(instructionLine) < 6:
            sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
            sys.exit()
        if instructionLine[2][0] != "at" or instructionLine[4][0] != "run":
            sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
            sys.exit()
        for day in instructionLine[1]:                                   # Checking for valid days
            if (day in days_of_week) == False:
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
            if instructionLine[1].count(day) > 1:
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
        for time in instructionLine[3]:               # Checking for valid times
            if instructionLine[3].count(time) > 1:                               # Checking for duplicate times
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
            if time.isdigit() == False:                                          # Checking for numeric values
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")   
                sys.exit()   
            if len(time) != 4:                                                   # Checking for correct length
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
            hour = int(time[:2])
            minute = int(time[2:])
            if hour < 0 or hour > 23:                                            # Checking for correct range
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
            if minute < 0 or minute > 59:
                sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                sys.exit()
        if instructionLine[0][0] == 'on':
            innerlist.append('once')                                     # If record is valid - append to list, each program which is to be run
        else:
            innerlist.append('every')
        i = 0
        while i < len(instructionLine[1]):
            innerlist.append(instructionLine[1][i])
            j = 0
            while j < len(instructionLine[3]):
                innerlist.append(instructionLine[3][j])
                innerlist.append(instructionLine[5])
                k = 6
                while k < len(instructionLine):
                    innerlist.append(instructionLine[k])
                    k += 1
                ls = []
                for item in innerlist:
                    ls.append(item)
                for record in run_at_list:
                    if record[1] == ls[1] and record[2] == ls[2]:                 # Checking for multiple programs running at the same time 
                        sys.stderr.write("error in configuration: " + lines[line_number] + "\n")
                        sys.exit()
                run_at_list.append(ls)
                while len(innerlist) != 2:
                    elem = innerlist[2]
                    innerlist.remove(elem)
                j += 1
            a = 1
            while a < len(innerlist):
                elem = innerlist[a]
                innerlist.remove(elem)
                a += 1
            i += 1
    else:
        sys.stderr.write("error in configuration: " + lines[line_number] + "\n")             # Invalid record - first word is not "on", "every" or "at"
        sys.exit()
    line_number += 1

i = 0
while i < len(run_at_list):
    j = 0
    while j < len(run_at_list[i]):                  # Changing list objects within run_at_list to the strings within them
        if type(run_at_list[i][j]) == list:
            elem = run_at_list[i][j][0]
            run_at_list[i][j] = elem
        j += 1
    i += 1

program_list = []
for program in run_at_list:                             # Creating a list of 'Record' objects of all programs which are to run
    if program[0] == 'at':
        params = ['ignored']                            # The first string given in a list of args to os.execv is ignored
        i = 3
        while i < len(program):
            params.append(program[i])
            i += 1
        today = datetime.date.today().strftime('%A')
        program_list.append(Records(program[0], today, program[1], program[2], params))
    else:
        params = ['ignored']                            # The first string given in a list of args to os.execv is ignored
        i = 4
        while i < len(program):
            params.append(program[i])
            i += 1
        program_list.append(Records(program[0], program[1], program[2], program[3], params))

def statusfile_message(list_of_programs):
    filename = "runner.status"
    try:
        file = open(filename)
    except FileNotFoundError:
        sys.stderr.write("file {} not found".format(filename) + "\n")
        sys.exit()
        
    file = open(filename, "w")

    for record in list_of_programs:
        time = record[1].datetime
        epoch = time.strftime('%s')

        if record[0] == "Success":
            file.write("ran " + Time.ctime(int(epoch)) + " " + record[1].program_path + " ")
            i = 1                                                                              # Start printing parameters from index 1 since the first parameter is ignored
            while i < len(record[1].parameters):
                file.write(record[1].parameters[i] + " ")
                i += 1
            file.write("\n")   

        if record[0] == "Error":
            file.write("error " + Time.ctime(int(epoch)) + " " + record[1].program_path + " ")
            i = 1
            while i < len(record[1].parameters):
                file.write(record[1].parameters[i] + " ")
                i += 1
            file.write("\n")  

        if record[0] == "not run":
            file.write("will run at " + Time.ctime(int(epoch)) + " " + record[1].program_path+ " ")  
            i = 1
            while i < len(record[1].parameters):
                file.write(record[1].parameters[i] + " ")
                i += 1
            file.write("\n")  

    file.close()

def time_val(record, days_of_week):
    today_index = int(datetime.datetime.today().strftime("%w"))
    run_at_day = days_of_week.index(record.day)

    if today_index > run_at_day:
        if today_index != 0:
            days_to_add = 7 - abs(today_index - run_at_day)
        else:
            days_to_add = abs(today_index - run_at_day)
    else:
        days_to_add = run_at_day - today_index
    
    run_at_date = datetime.datetime.today() + datetime.timedelta(days = days_to_add)

    current_day = datetime.datetime.now().day
    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute
    current_second = datetime.datetime.now().second
    current_microsecs = datetime.datetime.now().microsecond
    run_at_time = (record.time)
    run_at_hour = int(run_at_time[:2])
    run_at_minute = int(run_at_time[2:])

    if current_hour > run_at_hour:
        hours_to_add = run_at_hour - current_hour
    else:
        hours_to_add = run_at_hour - current_hour 
    run_at_date = run_at_date + datetime.timedelta(hours = hours_to_add)

    if current_minute > run_at_minute:
        minutes_to_add = run_at_minute - current_minute
    else:
        minutes_to_add = run_at_minute - current_minute
    run_at_date = run_at_date + datetime.timedelta(minutes = minutes_to_add)

    if current_second != 0:
        seconds_to_add = 0 - current_second
    run_at_date = run_at_date + datetime.timedelta(seconds = seconds_to_add)

    if current_microsecs != 0:
        microsecs_to_add = 100 - current_microsecs
    run_at_date = run_at_date + datetime.timedelta(microseconds = microsecs_to_add)

    if record.keyword == "at":                                                                                    # Checking if record is an 'at' record and if the time has passed, if so, changes time to next day
        if current_hour > run_at_hour or (current_hour == run_at_hour and current_minute > run_at_minute) or (current_hour == run_at_hour and current_minute == run_at_minute and current_second > 0):
            run_at_date = run_at_date + datetime.timedelta(days = 1)
            record.day = days_of_week[today_index + 1]
    else:                                                                                                         # Checking if record is an 'on' or 'every record and if the time has passed, if so, changes time to next week
        if (current_day == run_at_date.day and current_hour > run_at_hour) or (current_day == run_at_date.day and current_hour == run_at_hour and current_minute > run_at_minute) or (current_day == run_at_date.day and current_hour == run_at_hour and current_minute == run_at_minute and current_second > 0):
            run_at_date = run_at_date + datetime.timedelta(days = 7)

    record.datetime = run_at_date
    return run_at_date


raw_times = []
date_time_objs = []
for record in program_list:
    time = time_val(record, days_of_week)
    date_time_objs.append(time)
    epoch = datetime.datetime(time.year, time.month, time.day, time.hour, time.minute).strftime('%s')
    raw_times.append(epoch)


raw_times.sort()
sorted_program_list = []
for time in raw_times:
    i = 0
    while i < len(program_list):
        run_time = date_time_objs[i] 
        epoch = datetime.datetime(run_time.year, run_time.month, run_time.day, run_time.hour, run_time.minute).strftime('%s')
        if epoch == time:
            sorted_program_list.append(program_list[i])
        i += 1

def catch(signum, frame):
    statusfile_message(result_list)

for record in sorted_program_list:
    result_list.append(["not run", record])      # All programs initially recorded as 'not run'

while len(sorted_program_list) != 0:
    counter = 0
    signal.signal(signal.SIGUSR1, catch)         # Catching signal

    for raw_time in raw_times:
        time_difference = int(raw_time) - Time.time()

        Time.sleep(time_difference)              # Sleep until time to run next program
        try:
            pid = os.fork()
        except OSError:                          # Check for fork() errors
            result_list[0] = ["Error", sorted_program_list[0]]

        if pid > 0:                              # If in parent process then wait for child process to excute
            status = os.wait()
            
        elif pid == 0:                           
            try:
                os.execv(sorted_program_list[0].program_path, sorted_program_list[0].parameters)   # Run the program
            except OSError:
                sys.exit(1)                      # If program is not run then send signal to parent process to inidcate error
            
        elif pid < 0:
            result_list[0] = ["Error", sorted_program_list[0]]     
            
        if status[1] != 0:                                         # Checks the signal with which the child was terminated with, if not zero then an error occured
            result_list[0] = ["Error", sorted_program_list[0]]

        if sorted_program_list[0].keyword == "every":                                  # If record is an 'every' record, update the time to next week and add it to the end of the list
            updated_time = sorted_program_list[0].datetime + datetime.timedelta(days = 7)
            updated_record = Records('every', sorted_program_list[0].day, updated_time, sorted_program_list[0].program_path, sorted_program_list[0].parameters)
            sorted_program_list.append(updated_record)
        sorted_program_list.pop(0) 

sys.stderr.write("nothing left to run\n")
sys.exit()