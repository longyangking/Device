import numpy as np
from scipy.integrate import ode
from scipy.integrate import odeint

class ODE:
    '''
    Simulation for real/complex-valued ODE
    dy/dt = f(y,t0)
    '''
    def __init__(self,fun,y0,t0=0,jac=None,iscomplex=True,method='bdf'):
        self.fun = fun
        self.jac = jac
        
        self.y0 = y0
        self.t0 = t0
        self.method = method
        self.iscomplex = iscomplex

        self.system = None

    def set_method(self,method,iscomplex=True):
        methods = ['bdf','adams']
        if method not in methods:
            return False
        self.iscomplex = iscomplex
        self.method = method
        return True

    def set_fun(self,fun):
        self.fun = fun

    def set_jacobian(self,jac):
        self.jac = jac

    def set_initial_value(self,y0,t0):
        self.y0 = y0
        self.t0 = t0

    def init(self):
        self.system = ode(self.fun,self.jac)

        # set integrator
        code = 'vode'
        if self.iscomplex:
            code = 'zvode'
        self.system.set_integrator(code, method=self.method)

        self.system.set_initial_value(self.y0,self.t0)
        return self.system.successful()

    def evaluate(self,timesteps,step=False,relax=False):
        n_values = len(timesteps)
        values = list()
        status = True
        for i in range(n_values):
            t = timesteps[i]
            status = status and self.init()
            value = self.system.integrate(t,step,relax)
            values.append(value)
        return status, values

    def get_time(self):
        return self.system.t

class FastODE:
    '''
    Fast simulation, only for real-valued ODE
    '''
    def __init__(self,fun,y0):
        self.fun = fun
        self.y0 = y0

        self.system = None

    def set_fun(self,fun):
        self.fun = fun

    def set_initial_value(self,y0):
        self.y0 = y0

    def init(self):
        # Nothing, just for uniform call process like simulation class
        return True

    def evaluate(self,ts):
        solution = odeint(func=self.fun,y0=self.y0,t=ts)
        return solution

if __name__=='__main__':
    # Test simulation class
    print('Inner test: ODE')
    y0, t0 = [1.0j, 2.0], 0
    def fun(t,y):
        return [1j*2*y[0] + y[1], -2*y[1]**2]
    sim = ODE(fun=fun,y0=y0,t0=t0)
    print('ODE status: ',sim.init())

    # Test fastsimulation class
    print('Inner test: Fast ODE')
    def fun(y, t):
        theta, omega = y
        dydt = [omega, -0.25*omega - 5.0*np.sin(theta)]
        return dydt
    y0 = [np.pi-0.1,0.0]
    ts = np.linspace(0,10,101)
    sim = FastODE(fun=fun,y0=y0)
    print('Fast ODE status: ',sim.init())
    sol = sim.evaluate(ts)

    import matplotlib.pyplot as plt
    plt.plot(ts, sol[:, 0], 'b', label='theta(t)')
    plt.plot(ts, sol[:, 1], 'g', label='omega(t)')
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.show()