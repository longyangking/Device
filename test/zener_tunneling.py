import sys
sys.path.append("..")

import numpy as np
from device import system,hamiltonian

import matplotlib.pyplot as plt

v, delta = 0.2, 4

def onsite_func1(t):
    return v*t

def onsite_func2(t):
    return -v*t

def coupling_func(t):
    return delta, delta

if __name__=='__main__':
    point1 = system.Point(position=[0,0,0],onsite_func=onsite_func1)
    point2 = system.Point(position=[0,0,0],onsite_func=onsite_func2)
    link = system.Link(start_point=point1,end_point=point2,coupling_func=coupling_func)

    demo = system.System()
    demo.add_point(point1)
    demo.add_point(point2)
    demo.add_link(link)

    sim = hamiltonian.Hamiltonian(demo)
    init_state = [0,1]
    n_steps = 200
    timesteps = np.linspace(-1,1,n_steps)
    status, states = sim.evolve(timesteps=timesteps,init_state=init_state)
    
    state1 = [phi[0] for phi in states]
    state2 = [phi[1] for phi in states]
    plt.plot(timesteps,np.abs(state1),'b',label='State 1')
    plt.plot(timesteps,np.abs(state2),'r',label='State 2')
    plt.title('Tunneling between two states')
    plt.xlabel('Time')
    plt.ylabel('Probability')
    plt.ylim([-0.1,1.1])
    plt.legend()
    plt.show()