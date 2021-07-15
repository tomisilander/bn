#!/usr/bin/env python
import os, signal, re

# This is the pool flagging the signals

flags = set()

__signames__ = [s for s in dir(signal) if s.startswith("SIG")]

signums = dict(zip(__signames__,
                   (eval("signal.%s"%sn) for sn in __signames__)))
signams = dict(map(reversed, signums.items()))

# Call watch to register handlef for signum

def watch(signam, once=False) :

    def flagger(s,f):
        flags.add(signam)
    signal.signal(signums[signam], flagger)


# Send signal to a process after certain time

def wait_n_kill(time, signam, pid):

    def killer(s,f):
        os.kill(pid, signums[signam])
        
    signal.signal(signal.SIGALRM, killer)
    signal.alarm(time)


def wait_n_raise(time, signam):

    def raiser(s,f):
        flags.add(signam)
        
    signal.signal(signal.SIGALRM, raiser)
    signal.alarm(time)


# Helper function to turn "3h 4m" to seconds

def str2time(s):

    re_dhms = re.compile("([dhms])")

    t = 0
    t_lst = filter(lambda x:x, re_dhms.split(s.replace(" ","")))

    conv = {'d':24*3600, 'h':3600, 'm':60, 's':1}

    while t_lst:
        x = int(t_lst.pop(0))
        u = t_lst and t_lst.pop(0) or 's'

        t += x*conv[u]

    return t
