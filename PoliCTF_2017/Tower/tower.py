#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import re
import sys
import copy

s= None
maze= []
goal= (0, 0)
orientation= 0
path= ""

def connect():
    global s
    
    print "[+] connecting to server"
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #change host to 'localhost' and server maze.txt at port 31337 to host the challenge yourself
    s.connect(("tower.chall.polictf.it", 31337))
    
    #read initial data from server
    rsp= ""
    while not "(the lower left cell is 0,0)" in rsp:
        rsp= rsp+s.recv(1024)
        
    print "[+] received input"
    return rsp

def parse():
    global goal,maze
    
    inputData= connect()
    for line in inputData.splitlines():
        if len(line) < 2:
            continue
        if line.startswith("start"):
            continue
        if line.startswith("goal"):
            #parse goal coordinations
            line= line.split(" ")[1:]
            goal= (int(line[0][:-1]), int(line[1]))
            goal= coordToMaze(goal[0], goal[1])
            print "[+] parsed goal location: "+str(goal)
            break
        
        #store each line of the labyrinth as an element in the maze list
        maze.append(line[:-1])

#convert coordinates to position in maze datastructure
def coordToMaze(x,y):
    return ( 2*x+1 , len(maze)-y-1)

#put a marker into the maze datastructure where the goal is located
def setGoal(showMaze):
    x,y= goal
    showMaze[y]= showMaze[y][:x]+u"\u25A0"+showMaze[y][x+1:]
    return showMaze

def right(orientation):
    return (orientation +1) % 4

def left(orientation):
    return (orientation -1) % 4

def canMoveForward((x,y),orientation):
    if orientation == 0: #w
        return y > 0 and maze[y-1][x] != "_"
    if orientation == 1: #d
        return x<len(maze[0])-1 and maze[y][x+1] != "|"
    if orientation == 2: #s
        return y < len(maze) and maze[y][x] != "_"
    if orientation == 3: #a
        return x>0 and maze[y][x-1] != "|"

def moveForward(x,y,orientation):
    if orientation == 0: #w
        return x, y-1
    if orientation == 1: #d
        return x+2, y
    if orientation == 2: #s
        return x, y+1
    if orientation == 3: #a
        return x-2 , y

def invert(orientation):
    return (orientation+2)%4

def appendToPath(path, move):
    if len(path) == 0:
        return (path+move)
    lastMove= convertBack(path[-1])
    inverted= invert(lastMove)
    
    if inverted == convertBack(move):
        return path[:-1]
    
    return (path+move)
     
def walk(goalx, goaly):
    path= ""
    
    x,y = coordToMaze(0,0)
    orientation = 0
    while(x != goalx or y != goaly):
        orientation = right(orientation)
        while not canMoveForward((x,y),orientation):
            orientation= left(orientation)
            
        x,y = moveForward(x,y,orientation)
        move= convertOrientation(orientation)
        path= appendToPath(path, move)

    return path

def convertBack(orientation):
    if orientation == "w":
        return 0
    if orientation == "d":
        return 1
    if orientation == "s":
        return 2
    else:
        return 3

def convertOrientation(orientation):
    if orientation == 0:
        return "w"
    if orientation == 1:
        return "d"
    if orientation == 2:
        return "s"
    if orientation == 3:
        return "a"

def plotPath(path):
    showMaze= copy.deepcopy(maze)
    x,y= coordToMaze(0, 0)
    
    for move in path:
        x, y= moveForward(x, y, convertBack(move))
        symbol= "#"
        if showMaze[y][x] == "_":
            symbol= "#"
            
        showMaze[y]= showMaze[y][:x]+symbol+showMaze[y][x+1:]
        
    showMaze= setGoal(showMaze)
    print ""
    for line in showMaze:
        print line
    print ""
    
parse()
path= walk(goal[0], goal[1])
plotPath(path)
print "[+] Calculated path of length "+str(len(path))

s.send(path+"\n")

rsp= s.recv(1024)
flag= re.findall("flag\{.*\}", rsp)
if flag:
    print "[+] Acquired flag: "+flag[0]
else:
    print "[-] Failure: "+rsp


