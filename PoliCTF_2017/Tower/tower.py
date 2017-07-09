#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import re
import sys
import copy

goal= ""
maze= []
orientation= 0
path= ""
s= None

lineWidth= 81
numLines= 121

def connect():
    global s
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("tower.chall.polictf.it", 31337))
    
    rsp= ""
    while not "_" in rsp:
        rsp= s.recv(1024)
        
    line=""
    while not "start" in line:
        line= s.recv(1024)
        rsp= rsp+line
    
    print "Received input."
    return rsp


def coord_to_maze(x,y):
    return ( 2*x+1 , len(maze)-y-1)

def setGoal(showMaze):
    x,y= goal
    showMaze[y]= showMaze[y][:x]+u"\u25A0"+showMaze[y][x+1:]
    return showMaze

def printMaze(maze):
    
    print "width: "+str(len(maze[0]))
    print "height: "+str(len(maze))
    for line in maze:
        print line

def parse():
    global goal,maze
    
    inputData= connect()
    
    for line in inputData.splitlines():
        if line.startswith("start"):
            continue
        if line.startswith("goal"):
            line= line.split(" ")[1:]
            goal= (int(line[0][:-1]), int(line[1]))
            goal= coord_to_maze(goal[0], goal[1])
            print "Goal: "+str(goal)
            break
        
        maze.append(line[:-1])
        

def printCoord(x, y):
    x, y= coord_to_maze(x,y)
    print str(x)+", "+str(y)
    print maze[y][x]
    
def right(orientation):
    return (orientation +1) % 4


def left(orientation):
    return (orientation -1) % 4


def can_move_forward((x,y),orientation):
    if orientation == 0: #w
        return y > 0 and maze[y-1][x] != "_"
    if orientation == 1: #d
        return x<len(maze[0])-1 and maze[y][x+1] != "|"
    if orientation == 2: #s
        return y < len(maze) and maze[y][x] != "_"
    if orientation == 3: #a
        return x>0 and maze[y][x-1] != "|"

def move_forward(x,y,orientation):
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
     

def walk(goalx,goaly):
    path= ""
    count= 0
    
    x,y = coord_to_maze(0,0)
    orientation = 0
    while(x != goalx or y != goaly):
        orientation = right(orientation)
        while not can_move_forward((x,y),orientation):
            orientation= left(orientation)
            
        x,y = move_forward(x,y,orientation)
        move= convertOrientation(orientation)
        path= appendToPath(path, move)
        
        count+= 1
        if count < 13000:
            sys.stdout.write(convertOrientation(orientation))
        else:
            return path
        #sys.stdout.flush()
    
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
    x,y= coord_to_maze(0, 0)
    
    for move in path:
        x, y= move_forward(x, y, convertBack(move))
        symbol= "#"
        if showMaze[y][x] == "_":
            symbol= "#"
            
        showMaze[y]= showMaze[y][:x]+symbol+showMaze[y][x+1:]
        
    showMaze= setGoal(showMaze)
    printMaze(showMaze)
    
parse()
goalx= goal[0]
goaly= goal[1]
path= walk(goalx, goaly)
print path
plotPath(path)


print "Number of steps: "+str(len(path))
s.send(path+"\n")
for i in range(10):
    rsp= s.recv(1024)
    print str(rsp)


