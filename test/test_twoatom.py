import sys
sys.path.append("..")

import numpy as np
from device import system,hamiltonian

import matplotlib.pyplot as plt

def onsite_func1(t):
    return 2

def onsite_func2(t):
    return 1

def coupling_func(t):
    return 0.5,0.5

if __name__=='__main__':
    point1 = system.Point(position=[0,0,0],onsite_func=onsite_func1)
    point2 = system.Point(position=[0,0,0],onsite_func=onsite_func2)
    link = system.Link(start_point=point1,end_point=point2,coupling_func=coupling_func)

    demo = system.System()
    demo.add_point(point1)
    demo.add_point(point2)
    demo.add_link(link)

    sim = hamiltonian.Hamiltonian(demo)
    init_state = [1,0]
    n_steps = 51
    timesteps = np.linspace(0,5,n_steps)
    status, states = sim.evolve(timesteps=timesteps,init_state=init_state)
    
    state1 = [phi[0] for phi in states]
    state2 = [phi[1] for phi in states]
    plt.plot(timesteps,np.real(state1),'b',label='Atom 1')
    plt.plot(timesteps,np.real(state2),'r',label='Atom 2')
    plt.title('Coupling between two atoms')
    plt.xlabel('Time')
    plt.legend()
    plt.show()