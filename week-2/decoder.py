import numpy as np
from copy import deepcopy
import argparse
parser=argparse.ArgumentParser()

def dmap(action):
    if(action==0):
        print("N",end=" ")
    elif(action==1):
        print("E",end=" ")
    elif(action==2):
        print("S",end=" ")
    else:
        print("W",end=" ")

    return

def decode(gridfile,optimal_solution):
    grid = np.loadtxt(gridfile, dtype=int)
    nr = len(grid)
    nc = len(grid[0])
    n = nr * nc
    # actions N=0 E=1 S=2 W=3
    a = 4

    start = -1
    end = -1

    grid_coordinates_map = np.zeros((n, 2))

    k = 0
    while (k <= n - 1):
        for row in range(nr):
            for column in range(nc):
                grid_coordinates_map[k][0] = int(row)
                grid_coordinates_map[k][1] = int(column)
                k += 1

    for row in range(nr):
        for column in range(nc):
            if (grid[row][column] == 2):
                for state in range(n):
                    if (grid_coordinates_map[state][0] == row and grid_coordinates_map[state][1] == column):
                        start = state

    for row in range(nr):
        for column in range(nc):
            if (grid[row][column] == 3):
                for state in range(n):
                    if (grid_coordinates_map[state][0] == row and grid_coordinates_map[state][1] == column):
                        end = state

    solution=open(optimal_solution)
    data2=solution.readlines()

    #dmap(int(data2[start].split()[1]))

    state=start
    while(state!=end):
        row=int(grid_coordinates_map[state][0])
        column=int(grid_coordinates_map[state][1])
        dmap(int(data2[state].split()[1]))
        action=int(data2[state].split()[1])
        if(action==0):
            row-=1
        elif(action==1):
            column+=1
        elif(action==2):
            row+=1
        elif(action==3):
            column-=1

        for new_state in range(n):
            if (grid_coordinates_map[new_state][0] == row and grid_coordinates_map[new_state][1] == column):
                state=new_state







if __name__=="__main__":
    parser.add_argument("--grid",type=str)
    parser.add_argument("--value_policy",type=str)
    args=parser.parse_args()
    decode(args.grid,args.value_policy)
