import argparse
import numpy as np
import pulp
import re
from pulp import *
parser=argparse.ArgumentParser()


def give_answer_vi(filename):
    f=open(filename)
    data=f.readlines()
    end=[]
    if(data[-2].split()[1]=="episodic"):
        end = list(map(int, data[3].split()[1:]))
    n=int(data[0].split()[1])
    a=int(data[1].split()[1])
    start=int(data[2].split()[1])
    P=np.zeros((n,a,n))
    R=np.zeros((n,a,n))
    Q=np.zeros((n,a))
    if (data[-2].split()[1] == "episodic"):
        for i in end:
            for ac in range(a):
                P[i][ac][i]=1

    i=4
    while(data[i].split()[0]=="transition"):
        line=data[i].split()
        P[int(line[1])][int(line[2])][int(line[3])]= float(line[5])
        R[int(line[1])][int(line[2])][int(line[3])]= float(line[4])
        i+=1

    gamma=float(data[-1].split()[1])



    v=np.zeros(n)
    for i in range(n):
        v[i]=-1000
    for i in range(n):
        if i in end:
            v[i]=0


    epsilon=0.00000001

    c=1
    err=np.zeros(n)

    while (c==1):
        for s in range(n):
            err[s] = v[s]
            for ac in range(a):


                v[s]=max(v[s],gamma*np.dot(P[s][ac],v)+np.dot(P[s][ac],R[s][ac]))

        c=0

        for i in range(n):
            if(abs(v[i]-err[i])>=epsilon):
                c=1


    for s in range(n):
        for ac in range(a):
            Q[s][ac]=gamma*np.dot(P[s][ac],v)+np.dot(P[s][ac],R[s][ac])

    pi=np.zeros(n)
    Qn=np.zeros(n)

    for i in range(n):
        Qn[i]=-1000



    for s in range(n):
        max_index=0
        for ac in range(a):
            if(Qn[s]<Q[s][ac]):
                Qn[s]=Q[s][ac]
                max_index=ac
        pi[s]=max_index


    for i in range(n):
        print(v[i],end='\t')
        print(int(pi[i]))


def give_answer_hpi(filename):
    f=open(filename)
    data=f.readlines()
    end=[]
    if(data[-2].split()[1]=="episodic"):
        end = list(map(int, data[3].split()[1:]))
    n=int(data[0].split()[1])
    a=int(data[1].split()[1])
    start=int(data[2].split()[1])
    P=np.zeros((n,a,n))
    R=np.zeros((n,a,n))
    Q=np.zeros((n,a))
    if (data[-2].split()[1] == "episodic"):
        for i in end:
            for ac in range(a):
                P[i][ac][i]=1

    i=4
    while(data[i].split()[0]=="transition"):
        line=data[i].split()
        P[int(line[1])][int(line[2])][int(line[3])]= float(line[5])
        R[int(line[1])][int(line[2])][int(line[3])]= float(line[4])
        i+=1

    gamma=float(data[-1].split()[1])

    pi=np.zeros(n)
    epsilon=0.00001
    v = np.zeros(n)# Initialize state values to 0

    c=1

    Qn = np.zeros(n)

    while c==1:

        Ppi=np.zeros((n,n))
        Rpi=np.zeros((n,n))
        for s1 in range(n):
            for s2 in range(n):
                Ppi[s1][s2]=P[s1][int(pi[s1])][s2]
                Rpi[s2][s1]=R[s1][int(pi[s1])][s2]

        #ans1 evaluation to calculate P(pi)*R(pi) for policy evaluation
        ans=np.dot(Ppi, Rpi)
        ans1=np.zeros(n)

        for i in range(n):
            ans1[i]=ans[i][i]

        ni=np.zeros(n)
        err=np.zeros(n)
        v1=np.zeros(n)

        #policy evaluation
        if(np.linalg.det(np.identity(n)-gamma*Ppi)!=0):#if linear equation solvable
            for s in range(n):
                ni[s] = v[s]
            v = np.linalg.solve(np.identity(n) - gamma * Ppi, ans1)
        else:#else we need to apply iteration for policy evaluation
            for s in range(n):
                ni[s] = v[s]
                v1[s]= v[s]
            #max number of iteration of policy evaluation
            for j in range(100):
                max_diff = 0  # Initialize max difference
                for s in range(n):
                    err[s]=v[s]

                    # Compute state value
                v=ans1+gamma*np.dot(Ppi,v1)

                for s in range(n):
                    # Update maximum difference
                    max_diff = max(max_diff, abs(err[s] - v[s]))

                # If diff smaller than threshold delta for all states, algorithm terminates
                if max_diff < 0.000001:
                    break

        for s in range(n):
            for ac in range(a):
                Q[s][ac] = gamma * np.dot(P[s][ac], v) + np.dot(P[s][ac], R[s][ac])


        for s in range(n):
            Qn[s]=-100

        #policy improvement
        for s in range(n):
            max_index = 0
            for ac in range(a):
                if (Qn[s] < Q[s][ac]):
                    Qn[s] = Q[s][ac]
                    max_index = ac
            pi[s] = max_index


        for i in range(n):
            c=0
            if((abs(v[i]-ni[i]))>=epsilon):
                c=1

    for i in range(n):
        print(v[i],end="\t")
        print(int(pi[i]))





def give_answer_lp(filename):
    f=open(filename)
    data=f.readlines()
    end=[]
    if(data[-2].split()[1]=="episodic"):
        end = list(map(int, data[3].split()[1:]))
    n=int(data[0].split()[1])
    a=int(data[1].split()[1])
    start=int(data[2].split()[1])
    P=np.zeros((n,a,n))
    R=np.zeros((n,a,n))
    Q=np.zeros((n,a))
    if (data[-2].split()[1] == "episodic"):
        for i in end:
            for ac in range(a):
                P[i][ac][i]=1

    i=4
    while(data[i].split()[0]=="transition"):
        line=data[i].split()
        P[int(line[1])][int(line[2])][int(line[3])]= float(line[5])
        R[int(line[1])][int(line[2])][int(line[3])]= float(line[4])
        i+=1

    gamma=float(data[-1].split()[1])

    value_minimum_prob=pulp.LpProblem("optimal policy",LpMinimize)
    values=[]
    for s in range(n):
        variable=str('v'+str(s))
        variable=pulp.LpVariable(str(variable),lowBound=0,upBound=1,cat='Integer')
        values.append(variable)

    total_sum=""
    for v in values:
        total_sum+=v

    value_minimum_prob+=total_sum

    for i in range(n):
        for ac in range(a):
            value_minimum_prob+=values[i]-lpSum([(P[i][ac][j])*(R[i][ac][j]+gamma*values[j]) for j in range(n)])>=0

    value_minimum_prob.solve()

    print(" ----------------------------------------------")

    v=np.zeros(n)

    for i in range(n):
        v[i]=value(values[i])

    for s in range(n):
        for ac in range(a):
            Q[s][ac]=gamma*np.dot(P[s][ac],v)+np.dot(P[s][ac],R[s][ac])

    pi=np.zeros(n)
    Qn=np.zeros(n)

    for i in range(n):
        Qn[i]=-1000



    for s in range(n):
        max_index=0
        for ac in range(a):
            if(Qn[s]<Q[s][ac]):
                Qn[s]=Q[s][ac]
                max_index=ac
        pi[s]=max_index


    for i in range(n):
        print(v[i],end='\t')
        print(int(pi[i]))


























def value_function(filename,algo):
    if algo=="vi":
        give_answer_vi(filename)
    elif(algo=="hpi"):
        give_answer_hpi(filename)
    elif(algo=="lp"):
        give_answer_lp(filename)





if __name__=="__main__":
    parser.add_argument('--mdp',type=str)
    parser.add_argument('--algorithm',type=str)

    args=parser.parse_args()
    value_function(args.mdp,args.algorithm)

