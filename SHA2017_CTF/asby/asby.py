#!/usr/bin/python2

import os, sys, fcntl, time, subprocess
from subprocess import Popen, PIPE, STDOUT

def setNonBlocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def read(p):
    while True:
        try:
            out1 = p.stdout.read()
        except IOError:
            continue
        else:
            break
    return out1

p = Popen("./asby.exe", stdin = PIPE, stdout = PIPE, stderr = PIPE, bufsize = 1)
setNonBlocking(p.stdout)
setNonBlocking(p.stderr)

flag= "flag{" 
alphabet= "0123456789abcdef"

try:
    while 1:
        for ch in alphabet:
            found= False
            newFlag= flag+ch+"\n"
            sys.stdout.write("\r"+newFlag[:-1])
            p.stdin.write(newFlag)
            out1= read(p)
            time.sleep(0.05)
            
            if not "WRONG!" in out1:
                flag+= ch
                found= True
                break
        if not found:
            break

    flag+= "}"
    print "\nExtracted flag: "+flag
    p.stdin.write(flag+"\n")
    print read(p)

    print "\nFinished."
    p.kill()

except KeyboardInterrupt:            
    print "\nKilling asby.exe"
    p.kill()
    sys.exit()