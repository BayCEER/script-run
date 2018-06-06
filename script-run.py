#!/usr/bin/python -u 
import os
import signal
import sys
import time
import datetime
import subprocess
from thread import start_new_thread
import re
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

scripts=[]
pids={}
sigterm=False

restartscript=True
restartwait=5
markinterval=600


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    global sigterm
    sigterm=True
    for script, pid in pids.iteritems():
        killchilds(pid)
    time.sleep(0.01)
    logging.info("script-run stopped")
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


def killchilds(pid):
    p=subprocess.Popen("pgrep -P %d"%pid,shell=True, stdout=subprocess.PIPE).stdout
    pid_new = p.readline()
    p.close()
    if(pid_new):
        pid_new=int(pid_new)
        killchilds(pid_new)
    logging.info(" Stopping %d"%pid)
    os.kill(pid, signal.SIGTERM)
    try:
        os.waitpid(pid,0)
    except OSError:
        pass

def start_script(script):
    global pids
    while(not sigterm):
        p=subprocess.Popen(script,shell=True,stderr=sys.stderr)
        pids[script]=p.pid
        logging.info("started "+script+" with pid %d"%p.pid)
        p.wait()
        if(not sigterm):
            pids.pop(script)
            logging.info(script+" with pid %d stopped unexpectedly"%p.pid)
            if(not restartscript):
                logging.info("restart of "+script+" disabled")
                break
            time.sleep(restartwait)
        
    logging.info("stopped "+script+" with pid %d"%p.pid)
    
    
print(" script-run started")

with open('/etc/script-run.conf') as f:
    for line in f:
        line=line.rstrip()
        t=line.split("#")
        # ignore all lines shorter than 2
        if(len(t[0])<=1):
            continue
        t2=re.split(" *= *",t[0])
        # Configsettings
        if(t2[0] in ['restartscript','restartwait','markinterval']):
            t2[1]=t2[1].strip().lower()
            if(t2[0]=='restartscript'):
                restartscript=not (t2[1] in ['0','no','false'])
                logging.info('found config restartscript: %r'%restartscript)
            elif(t2[0]=='restartwait'):
                restartwait=int(t2[1])
                logging.info('found config restartwait: %d'%restartwait)
            elif(t2[0]=='markinterval'):
                markinterval=int(t2[1])
                logging.info('found config markinterval: %d'%markinterval)
            continue
        # Scripts
        t2=t[0].split(" ")
        if(os.access(t2[0],os.X_OK)):
            scripts.append(t[0])
        else:
            logging.critical("%s is not executable"%t2[0])



for s in scripts:
    start_new_thread(start_script, (s,))

while(True):
    time.sleep(1)
    if(int(time.time())%markinterval==0):
        logging.info(" ------- MARK -----") 

