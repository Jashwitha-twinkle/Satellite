import numpy as np
from physics.j2propogator import acceleration_total

def rk4_step(state, dt):

    r = state[:3]
    v = state[3:]

    def derivative(s):
        s = np.array(s, dtype=float) 
        r = s[:3]
        v = s[3:]

        a = acceleration_total(r)

        return np.concatenate([v, a])

    k1 = derivative(state)
    k2 = derivative(state + 0.5*dt*k1)
    k3 = derivative(state + 0.5*dt*k2)
    k4 = derivative(state + dt*k3)

    return state + dt/6*(k1 + 2*k2 + 2*k3 + k4)