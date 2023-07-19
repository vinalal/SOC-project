import numpy as np
from copy import deepcopy
import argparse
parser=argparse.ArgumentParser()


def encode(gridfile):
    grid=np.loadtxt(gridfile,dtype=int)
    nr=len(grid)
    nc=len(grid[0])
    n=nr*nc
    # actions N=0 E=1 S=2 W=3
    a=4

    start=-1
    end=-1


    grid_coordinates_map=np.zeros((n,2))

    k=0
    while(k<=n-1):
        for row in range(nr):
            for column in range(nc):
                grid_coordinates_map[k][0]=int(row)
                grid_coordinates_map[k][1]=int(column)
                k+=1

    for row in range(nr):
        for column in range(nc):
            if(grid[row][column]==2):
                for state in range(n):
                    if(grid_coordinates_map[state][0]==row and grid_coordinates_map[state][1]==column):
                        start=state

    for row in range(nr):
        for column in range(nc):
            if(grid[row][column]==3):
                for state in range(n):
                    if(grid_coordinates_map[state][0]==row and grid_coordinates_map[state][1]==column):
                        end=state
        

    P=np.zeros((n,a,n))
    R=np.zeros((n,a,n))
    for s in range(n):
        for ac in range(a):
            for s_final in range(n):
                R[s][ac][s_final]=-1


    for s in range(n):
        if(grid_coordinates_map[s][0]>=1 and grid_coordinates_map[s][0]<=nr-2 and grid_coordinates_map[s][1]>=1 and grid_coordinates_map[s][1]<=nc-2):
            r=int(grid_coordinates_map[s][0])
            c=int(grid_coordinates_map[s][1])
            for ac in range(a):
                if(ac==0):
                    if grid[r-1][c] == 1:
                        P[s][ac][s]=1
                    elif grid[r-1][c] ==0 or grid[r-1][c]==2 or grid[r-1][c]==3:
                        cr=deepcopy(grid_coordinates_map[s])
                        cr[0]-=1
                        s_final = np.where((grid_coordinates_map == cr).all(axis=1))[0][0]
                        P[s][ac][s_final]=1

                elif ac==1:
                    if grid[r][c+1] == 1:
                        P[s][ac][s] = 1
                    elif grid[r][c+1] ==0 or grid[r][c+1]==2 or grid[r][c+1]==3:
                        cr = deepcopy(grid_coordinates_map[s])
                        cr[1] += 1
                        s_final = np.where((grid_coordinates_map == cr).all(axis=1))[0][0]
                        P[s][ac][s_final] = 1

                elif ac==2:
                    if grid[r+1][c] == 1:
                        P[s][ac][s] = 1
                    elif grid[r+1][c] ==0 or grid[r+1][c]==2 or grid[r+1][c]==3:
                        cr = deepcopy(grid_coordinates_map[s])
                        cr[0] += 1
                        s_final = np.where((grid_coordinates_map == cr).all(axis=1))[0][0]
                        P[s][ac][s_final] = 1


                elif ac==3:
                    if grid[r][c-1] == 1:
                        P[s][ac][s] = 1
                    elif grid[r][c-1] ==0 or grid[r][c-1]==2 or grid[r][c-1]==3:
                        cr = deepcopy(grid_coordinates_map[s])
                        cr[1] -= 1
                        s_final = np.where((grid_coordinates_map == cr).all(axis=1))[0][0]
                        P[s][ac][s_final] = 1


    print("numStates",n)
    print("numActions",a)
    print("Start",start)
    print("end",end)
    for s in range(n):
        for ac in range(a):
            for s_final in range(n):
                if(P[s][ac][s_final]!=0):
                    print("transition",s,ac,s_final,R[s][ac][s_final],P[s][ac][s_final])
    print("mdptype episodic")
    print("discount  1.0")






if __name__=="__main__":
    parser.add_argument("--grid",type=str)
    args=parser.parse_args()
    encode(args.grid)



