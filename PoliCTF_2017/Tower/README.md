# PoliCTF 2017 - **Tower**
`Grab Bag` `154pts` `74 solves`

<br />

## Description
You are entering a Lab where you will be the experiment

`nc tower.chall.polictf.it 31337`

<br />

## Overview
After connecting to the given service via netcat, we are presented with a random labyrinth, our start coordinates (which are always at [0,0]) and the coordinates of the goal that we have to reach:
```bash
[...]
|   | |_ _|_|   |  _|_  |  _  |  _ _| |_  | | | | | |_|_  |_  | |   | |_|_ _| |_| 
| |_|  _   _ _|    _   _|  _| | |   | | |_ _| |         |_ _ _    |   | | | |_  | 
|   |  _|_ _|   |_ _|_| |  _| |   |  _|_ _  |  _|_| | | | |_  |_| |_| |_  | |_  | 
| |_| | |  _ _|  _  | |  _ _| | | |  _|_ _  |  _|_  | |_| | | | |_|_ _|   | |  _| 
|  _|  _|    _| |   | | | | | |_| |_ _ _  | | |_  |_|_    |_ _ _ _  | | |   |_  | 
|_ _|_ _|_|_ _|_|_|_ _ _ _ _|_ _ _ _|_ _ _ _|_ _ _ _ _|_|_ _ _ _ _ _ _|_|_|_ _ _| 
start: 0, 0
goal: 24, 68
Use wasd to write the path you want to take (w up, s down, ...)
(the lower left cell is 0,0)
```
We can navigate through the labyrinth by sending `w` `a` `s` `d` and are not allowed to hit a wall, otherwise we get the message: _"You hit a wall, you lose"_ and the connection is closed. Besides this message, we don't get any feedback from the server about our progress. Overall, it is pretty clear what we have to do:
* Read and process the labyrinth and the goal location
* Write an algorithm that calculates a path from the start location to the goal location
* Send the path to the service and receive the flag

<br />

## Solution
> **Note:** The full solution source code can be found under `PoliCTF_2017/tower/tower.py`

### Labyrinth processing


### Path finding algorithm


### Getting the flag


```
Number of steps: 220
Ehi!! You're still in the lab!! Where are you going?!?
```

