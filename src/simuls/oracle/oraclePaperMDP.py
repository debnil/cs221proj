""" value iteration to solve the decision making for the problem of traffic junction """
from pylab import zeros
from scipy import factorial
from math import exp,fabs
import random
m=20 #the maximum value of m (the number of waiting cars at the NS road)
n=20 #the maximum value of n (the number of waiting cars at the WE road)
N=2*(m+1)*(n+1) #the number of possible states of the system
gamma=0.8 # discout factor
theta=10e-10 #small number to stop the loop in the value iteration
Cross_state=[’N-S open’,’E-W open’]
#-----------------------------------------------------------------------------------------------------
#definition of the set of states
def states(m,n):
	'''The entire state of the system is represented by a list composed of each
	possible state of the system. Then, each possible state is a list composed of
	the state of the cross, the number of circulating cars, and the number of
	waiting cars'''
	state=[]
	for elt in Cross_state:
		for non_stop in range (m+1):
			for stop in range (n+1):
				state.append([elt,non_stop,stop])
	return state
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#definition of the reward function
def reward_function(state):
	'''The reward is represented as a vector. Each component is the reward that one has for each state.
	This function is returning two such vectors, according to the two possible actions taken'''
	reward_change=[]
	reward_stay=[]
	for i in range (len(state)/2): #for all the states such that N-S is open
		if (state[i][2]>=2*(state[i][1])):
			reward_change.append(1)
			reward_stay.append(0)
		else:
			reward_change.append(-1)
			reward_stay.append(1)
	for i in range ((len(state))/2,len(state)): #for all the states such that W_E is open
		if (state[i][1]>=2*(state[i][2])):
			reward_change.append(1)
			reward_stay.append(0)
		else:
			reward_change.append(-1)
			reward_stay.append(1)
	return reward_change,reward_stay
#---------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#definition of the transition probability for the action change
def transistion_probability_for_change(state):
	'''The transition probability is a matrix for each action to be taken.
	The columns are the following possible state if taking an action, and
	the rows are the previous states of the system. This function returns
	the matrix when taking the action Change'''
	c=[]
	for i in range (len(state)):
		ci=0
		for j in range(len(state)):
			if state[i][0]!=state[j][0]:
				if (state[j][1]==state[i][1] and state[j][2]==state[i][2]+1)==True:
					ci=ci+1
				if (state[j][1]==state[i][1] and state[j][2]==state[i][2]-1)==True:
					ci=ci+1
				if (state[j][1]==state[i][1]+1 and state[j][2]==state[i][2]+1)==True:
					ci=ci+1
				if (state[j][1]==state[i][1]+1 and state[j][2]==state[i][2]-1)==True:
					ci=ci+1
				if (state[j][1]==state[i][1]+1 and state[j][2]==state[i][2])==True:
					ci=ci+1
				if (state[j][1]==state[i][1]-1 and state[j][2]==state[i][2]+1)==True:
					ci=ci+1
				if (state[j][1]==state[i][1]-1 and state[j][2]==state[i][2]-1)==True:
					ci=ci+1
				if (state[j][1]==state[i][1]-1 and state[j][2]==state[i][2])==True:
					ci=ci+1
		c.append(ci)

	P_change=zeros([len(state),len(state)])
	for i in range (len(state)):
		for j in range (len(state)):
			if state[i][0]==state[j][0]:
				P_change[i,j]=0
			else:
				if (state[j][1]==state[i][1] and state[j][2]==state[i][2]):
					P_change[i,j]=1.0/2
				else:
					if (state[j][1]==state[i][1] and
					state[j][2]==state[i][2]+1)
					or(state[j][1]==state[i][1] and
					state[j][2]==state[i][2]-1) or
					(state[j][1]==state[i][1]+1 and
					state[j][2]==state[i][2]+1) or
					(state[j][1]==state[i][1]+1 and
					state[j][2]==state[i][2]-1) or
					(state[j][1]==state[i][1]+1 and
					state[j][2]==state[i][2]) or
					(state[j][1]==state[i][1]-1 and
					state[j][2]==state[i][2]+1) or
					(state[j][1]==state[i][1]-1 and
					state[j][2]==state[i][2]-1) or
					(state[j][1]==state[i][1]-1 and
					state[j][2]==state[i][2]):
						P_change[i,j]=1.0/(2*c[i])
					else:
						P_change[i,j]=0
	return P_change
#------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#definition of the transition probability for the action Stay
def transistion_probability_for_stay(state):
	'''The transition probability is a matrix for each action to be taken.The columns are
	the following possible state if taking an action, and the rows are the previous states
	of the system. This function returns the matrix when taking the action Stay'''
	d=[]
	for i in range (len(state)):
		di=0
		for j in range(len(state)):
			if state[i][0]==state[j][0]:
				if (state[j][1]==state[i][1]-2 and
				(state[j][2]==state[i][2]-2 or
				state[j][2]==state[i][2]-1 or
				state[j][2]==state[i][2] or
				state[j][2]==state[i][2]+2 or
				state[j][2]==state[i][2]+1))==True:
					di=di+1
				if (state[j][1]==state[i][1]-1 and
				(state[j][2]==state[i][2]-2 or
				state[j][2]==state[i][2]-1 or
				state[j][2]==state[i][2] or
				state[j][2]==state[i][2]+2 or
				state[j][2]==state[i][2]+1))==True:
					di=di+1
				if (state[j][1]==state[i][1] and
				(state[j][2]==state[i][2]-2 or
				state[j][2]==state[i][2]-1 or
				state[j][2]==state[i][2] or
				state[j][2]==state[i][2]+2 or
				state[j][2]==state[i][2]+1)) ==True:
					di=di+1
				if (state[j][1]==state[i][1]+2 and
				(state[j][2]==state[i][2]-2 or
				state[j][2]==state[i][2]-1 or
				state[j][2]==state[i][2] or
				state[j][2]==state[i][2]+2 or
				state[j][2]==state[i][2]+1)) ==True:
					di=di+1
				if (state[j][1]==state[i][1]+1 and
				(state[j][2]==state[i][2]-2 or
				state[j][2]==state[i][2]-1 or
				state[j][2]==state[i][2] or
				state[j][2]==state[i][2]+2 or
				state[j][2]==state[i][2]+1)) ==True:
					di=di+1
		d.append(di)
	P_stay=zeros([len(state),len(state)])
	for i in range (len(state)):
		for j in range (len(state)):
			if (2<=state[i][1]<=m-2 and 2<=state[i][2]<=n-2 ):
				if state[i][0]!=state[j][0]:
					P_stay[i,j]=0
				else:
					if state[i][0]==’N-S open’:
						P_m=0
						P_n=0
						if state[j][1]==(state[i][1]-2):
							P_m=3.0/16
						if state[j][1]==state[i][1]-1:
							P_m=9.0/32
						if state[j][1]==state[i][1]:
							P_m=9.0/32
						if state[j][1]==state[i][1]+2:
							P_m=1.0/12
						if state[j][1]==state[i][1]+1:
							P_m=2.0/12
						if state[j][2]==state[i][2]-2:
							P_n=(1.0/3)*(1.0/20)
						if state[j][2]==state[i][2]-1:
							P_n=(2.0/3)*(1.0/20)
						if state[j][2]==state[i][2]:
							P_n=(3.0/8)*(19.0/20)
						if state[j][2]==state[i][2]+2:
							P_n=(1.0/4)*(19.0/20)
						if state[j][2]==state[i][2]+1:
							P_n=(3.0/8)*(19.0/20)
						P_stay[i][j]=P_n*P_m
					else:
						P_m=0
						P_n=0
						if state[j][2]==(state[i][2]-2):
							P_n=3.0/16
						if state[j][2]==state[i][2]-1:
							P_n=9.0/32
						if state[j][2]==state[i][2]:
							P_n=9.0/32
						if state[j][2]==state[i][2]+2:
							P_n=1.0/12
						if state[j][2]==state[i][2]+1:
							P_n=2.0/12
						if state[j][1]==state[i][1]-2:
							P_m=(1.0/3)*(1.0/20)
						if state[j][1]==state[i][1]-1:
							P_m=(2.0/3)*(1.0/20)
						if state[j][1]==state[i][1]:
							P_m=(3.0/8)*(19.0/20)
						if state[j][1]==state[i][1]+2:
							P_m=(1.0/4)*(19.0/20)
						if state[j][1]==state[i][1]+1:
							P_m=(3.0/8)*(19.0/20)
						P_stay[i][j]=P_m*P_n
			else:
				if state[i][0]!=state[j][0]:
					P_stay[i,j]=0
				else:
					if (state[j][1]==state[i][1]-2 and
						(state[j][2]==state[i][2]-2 or
						state[j][2]==state[i][2]-1 or
						state[j][2]==state[i][2] or
						state[j][2]==state[i][2]+2 or
						state[j][2]==state[i][2]+1)) or (
					state[j][1]==state[i][1]-1 and
						(state[j][2]==state[i][2]-2 or
						state[j][2]==state[i][2]-1 or
						state[j][2]==state[i][2] or
						state[j][2]==state[i][2]+2 or
						state[j][2]==state[i][2]+1)) or (
					state[j][1]==state[i][1] and
						(state[j][2]==state[i][2]-2 or
						state[j][2]==state[i][2]-1 or
						state[j][2]==state[i][2] or
						state[j][2]==state[i][2]+2 or
						state[j][2]==state[i][2]+1)) or(
					state[j][1]==state[i][1]+2 and
						(state[j][2]==state[i][2]-2 or
						state[j][2]==state[i][2]-1 or
						state[j][2]==state[i][2] or
						state[j][2]==state[i][2]+2 or
						state[j][2]==state[i][2]+1)) or(
					state[j][1]==state[i][1]+1 and
						(state[j][2]==state[i][2]-2 or
						state[j][2]==state[i][2]-1 or
						state[j][2]==state[i][2] or
						state[j][2]==state[i][2]+2 or
						state[j][2]==state[i][2]+1)):
						
						P_stay[i][j]=1.0/d[i]
	return P_stay

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#value iteration algorithm
def value_iteration(state,reward1,reward2,probability_change,probability_stay,action):
	'''This is computing the policy which is a map from each possible states of the system
	to the action that should be taken. It returns a dictionary in which keys are the states
	and the values are the corresponding action to take'''

	V = []
	v0 = []
	for ii in range(len(state)): #construction of V[0]
		v0.append(0)
	V.append(v0)
	i=1
	Stop=False
	while (Stop==False): #construction of V[i] until convergence
		vi = []
		diff=[]
		action_taken=[]
		condition=True
		for j in range (len(state)): #construction of each component of v[i],
									#each component corresponds to one state
			sum_change=0
			sum_stay=0
			for k in range (len(state)):#calculation of the sumation
				sum_change = sum_change + ((probability_change[j][k])*(V[i-1][k]))
				sum_stay = sum_stay + ((probability_stay[j][k])*(V[i-1][k]))
			Q_change=reward1[j]+(gamma*sum_change) #the value function for the action ’change’
			Q_stay=reward2[j]+(gamma*sum_stay) #the value function for the action ’stay’
			#finding the maximum of the value functions according to the two actions
			if (Q_change>Q_stay):
				vi.append(Q_change)
				action_taken.append(action[0])
			if (Q_stay>Q_change):
				vi.append(Q_stay)
				action_taken.append(action[1])
			if (Q_change==Q_stay):
				tmp=random.choice([Q_change,Q_stay])
				vi.append(tmp)
				if tmp==Q_change:
					action_taken.append(action[0])
				else:
					action_taken.append(action[1])
			diff.append(fabs(vi[j]-V[i-1][j])) #construction of a vector of the difference
			condition=condition and fabs(vi[j]-V[i-1][j])<theta
		V.append(vi)
		if (condition==True):
			print ’The iteration has stopped at step’,i
			Stop=True
			#construction of the dictionary of policy
			decision={}
			for i in range (len(state)):
				decision[str(state[i])]=action_taken[i]
				#write the correspondence state-action in a file
				decisionmaking=open(’decisionfile.dat’,’a’)
				text=str(state[i][0])+’,’+ str(state[i][1])+’,’+str(state[i][2])+’,’+str(action_taken[i])+’\n’
				decisionmaking.write(text)
				decisionmaking.close()
			print decision
		else:
			i=i+1
	return decision

# main ===============================================
if __name__ == "__main__":
	set_of_state=states(m,n)
	print "Set of states"
	print set_of_state
	print 'The number of possible state is',len(set_of_state)
	action=['Change','Stay the same']
	set_of_rewardch,set_of_rewardst=reward_function(set_of_state)
	print ’Vector of rewards for the action change’
	print set_of_rewardch
	print ’Vector of rewards for the action stay’
	print set_of_rewardst
	P_change=transistion_probability_for_change(set_of_state)
	print ’transition probability for change’
	print P_change
	P_stay=transistion_probability_for_stay(set_of_state)
	print ’Transition probability for stay’
	print P_stay
	d=value_iteration(set_of_state,set_of_rewardch,set_of_rewardst,P_change,P_stay,action)