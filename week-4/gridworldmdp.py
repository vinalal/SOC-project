import numpy as np
import matplotlib.pyplot as plt

coordinate_map = np.zeros((70, 2))
n = 70
s = 0
while (s <= n - 1):
    for row in range(7):
        for column in range(10):
            coordinate_map[s][0] = int(row)
            coordinate_map[s][1] = int(column)
            s += 1
end=[3,7]
end_state=-1
for s in range(n):
    if(coordinate_map[s][0]==end[0] and coordinate_map[s][1]==end[1]):
        end_state=s





def next_state_reward(s,a):
    coordinates=[coordinate_map[s][0],coordinate_map[s][1]]
    air = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
    air_here = air[int(coordinates[1])]
    if(s==end_state):
        return(coordinates,0)
    if(a==0):
        if(coordinates[0]-1-air_here<0):
            coordinates[0]=0
        else:
            coordinates[0]-=(1+air_here)
    elif(a==2):
        if(coordinates[0]+1-air_here>6):
            coordinates[0]=6
        elif(coordinates[0]+1-air_here<0):
            coordinates[0]=0
        else:
            coordinates[0]-=(-1+air_here)
    elif(a==1):
        if(coordinates[0]-air_here<0):
            coordinates[0]=0
        else:
            coordinates[0]-=air_here

        if(coordinates[1]<=8):
            coordinates[1]+=1

    elif(a==3):
        if (coordinates[0] - air_here < 0):
            coordinates[0] = 0
        else:
            coordinates[0]-=air_here

        if(coordinates[1]>=1):
            coordinates[1]-=1



    final_state=-1
    for i in range(n):
        if coordinate_map[i][0]==coordinates[0] and coordinate_map[i][1]==coordinates[1] :
            final_state=i
    return final_state,-1

def sarsa():
    x=[]
    y=[]
    counter_step=0
    counter_episode=0
    q=np.zeros((n,4))

    m=4
    epsilon=0.5
    alpha=0.1 #learning rate
    #this was suitable to get convergence to right values
    '''The learning rate determines how much the agent updates its q values based on new information. 
    A higher learning rate can lead to faster convergence, but it may also introduce more instability or overshooting. 
    On the other hand, a lower learning rate allows for more cautious updates, 
    which can help smooth out the learning process and stabilize the behavior.'''

    for i in range(8000):
        counter_episode+=1
        s=30
        actionss=[0,1,2,3]
        '''max_a=np.argmax(q[s])
        prob=[0,0,0,0]
        for i in range(4):
            if(i!=max_a):
                prob[i]=epsilon/m
            else:
                prob[i]=epsilon/m + 1 - epsilon
    
        act=int(np.random.choice(actionss,1,p=[prob[0],prob[1],prob[2],prob[3]]))
        this is not a wrong method but we will have to adjust epsilon and alpha correctly'''
        act = 0
        if np.random.uniform(0, 1) < epsilon:
            act = np.random.choice(actionss)
        else:
            act = np.argmax(q[s, :])
        while(s!=end_state):
            counter_step+=1
            ans=next_state_reward(s,act)
            r=ans[1]
            s1=ans[0]
            '''max_a1=list(q[s]).index(max(list(q[s])))
            prob1=[0,0,0,0]
            for i in range(4):
                if(i!=max_a1):
                    prob1[i]=epsilon/m
                else:
                    prob1[i]=epsilon/m + 1 - epsilon
            next_act=int(np.random.choice(actionss,1,p=[prob1[0],prob1[1],prob1[2],prob1[3]]))'''
            next_act = 0
            if np.random.uniform(0, 1) < epsilon:
                next_act = np.random.choice(actionss)
            else:
                next_act = np.argmax(q[s, :])
            q[s][act]=q[s][act]+alpha*(r+0.99*q[s1][next_act]-q[s][act])
            s=s1
            act=next_act

            if(counter_step%1000)==0:
                x.append(counter_step)

        if (counter_episode%10)==0:
            y.append(counter_episode)

    min_length=min(len(x),len(y))

    plt.plot(x[:min_length], y[:min_length], '-o')  # '-o' adds markers at each data point
    plt.ylabel('Number of Episodes')
    ax = plt.gca()
    ax.set_yscale('log')
    ax1=plt.gca()
    ax1.set_xscale('log')
    plt.xlabel('Total Number of Steps Taken')
    plt.title('Learning Progress')
    plt.show()



    solution=np.zeros(n)
    print(q[30])

    for s in range(n):
        max_index=np.argmax(q[s])
        solution[s]=max_index

    state=30
    count=0

    for i in range(100):
        count+=1
        print(solution[state])
        ans=next_state_reward(state,solution[state])
        state=ans[0]
        if(state==end_state):
            break
    print(count)

def expected_sarsa():
    x = []
    y = []
    counter_step = 0
    counter_episode = 0
    q = np.zeros((n, 4))

    m = 4
    epsilon = 0.5
    alpha = 0.1  # learning rate
    # this was suitable to get convergence to right values
    '''The learning rate determines how much the agent updates its q values based on new information. 
    A higher learning rate can lead to faster convergence, but it may also introduce more instability or overshooting. 
    On the other hand, a lower learning rate allows for more cautious updates, 
    which can help smooth out the learning process and stabilize the behavior.'''

    for i in range(5000):
        counter_episode += 1
        s = 30
        actionss = [0, 1, 2, 3]
        '''max_a=np.argmax(q[s])
        prob=[0,0,0,0]
        for i in range(4):
            if(i!=max_a):
                prob[i]=epsilon/m
            else:
                prob[i]=epsilon/m + 1 - epsilon

        act=int(np.random.choice(actionss,1,p=[prob[0],prob[1],prob[2],prob[3]]))
        this is not a wrong method but we will have to adjust epsilon and alpha correctly'''
        act = 0
        if np.random.uniform(0, 1) < epsilon:
            act = np.random.choice(actionss)
        else:
            act = np.argmax(q[s, :])
        while (s != end_state):
            counter_step += 1
            ans = next_state_reward(s, act)
            r = ans[1]
            s1 = ans[0]
            max_a1=list(q[s]).index(max(list(q[s])))
            prob1=[0,0,0,0]
            for i in range(4):
                if(i!=max_a1):
                    prob1[i]=epsilon/m
                else:
                    prob1[i]=epsilon/m + 1 - epsilon
            next_act = 0
            if np.random.uniform(0, 1) < epsilon:
                next_act = np.random.choice(actionss)
            else:
                next_act = np.argmax(q[s, :])


            target=0
            for i in range(4):
                target+=prob1[i]*q[s][i]

            q[s][act] = q[s][act] + alpha * (r + 0.99 * target - q[s][act])
            s = s1
            act = next_act

            if (counter_step % 1000) == 0:
                x.append(counter_step)

        if (counter_episode % 10) == 0:
            y.append(counter_episode)

    min_length = min(len(x), len(y))

    plt.plot(x[:min_length], y[:min_length], '-o')  # '-o' adds markers at each data point
    plt.ylabel('Number of Episodes')
    ax = plt.gca()
    ax.set_yscale('log')
    ax1 = plt.gca()
    ax1.set_xscale('log')
    plt.xlabel('Total Number of Steps Taken')
    plt.title('Learning Progress')
    plt.show()

    solution = np.zeros(n)
    print(q[30])

    for s in range(n):
        max_index = np.argmax(q[s])
        solution[s] = max_index

    state = 30
    count = 0

    for i in range(100):
        count += 1
        print(solution[state])
        ans = next_state_reward(state, solution[state])
        state = ans[0]
        if (state == end_state):
            break
    print(count)


def Q_learn():
    x=[]
    y=[]
    counter_step=0
    counter_episode=0
    q=np.zeros((n,4))

    m=4
    epsilon=0.5
    alpha=0.1 #learning rate
    #this was suitable to get convergence to right values

    for i in range(200):
        counter_episode+=1
        s=30
        actionss=[0,1,2,3]

        while(s!=end_state):
            counter_step+=1
            act = 0
            if np.random.uniform(0, 1) < epsilon:
                act = np.random.choice(actionss)
            else:
                act = np.argmax(q[s, :])

            ans=next_state_reward(s,act)
            s1=ans[0]
            r=ans[1]

            q[s][act]=q[s][act]+alpha*(r+0.9*q[s1][np.argmax(q[s1,:])]-q[s][act])
            s=s1

            if(counter_step%1000)==0:
                x.append(counter_step)

        if (counter_episode%10)==0:
            y.append(counter_episode)

    min_length=min(len(x),len(y))

    plt.plot(x[:min_length], y[:min_length], '-o')  # '-o' adds markers at each data point
    plt.ylabel('Number of Episodes')
    plt.xlabel('Total Number of Steps Taken')
    plt.title('Learning Progress')
    plt.show()



    solution=np.zeros(n)
    print(q[30])

    for s in range(n):
        max_index=np.argmax(q[s])
        solution[s]=max_index

    state=30
    count=0

    for i in range(100):
        count+=1
        print(solution[state])
        ans=next_state_reward(state,solution[state])
        state=ans[0]
        if(state==end_state):
            break
    print(count)


Q_learn()








