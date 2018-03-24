import numpy as np 
from .solver import ODE

class Hamiltonian:
    def __init__(self,system):
        self.system = system

    def evolve(self,timesteps,init_state):
        y0, t0 = init_state,timesteps[0]
        sim = ODE(fun=self._fun,y0=y0,t0=t0)
        status, states = sim.evaluate(timesteps)
        return status, states

    def _fun(self,t,y):
        hamiltonian = self.system.get_hamiltonian(t)
        _array = list()
        n_sites = self.system.get_n_sites()
        for i in range(n_sites):
            value = -1j*np.sum([hamiltonian[i,j]*y[j] for j in range(n_sites)])
            _array.append(value)
        return _array
                
    def eigenvalues(self):
        pass

    def eigensystem(self):
        pass