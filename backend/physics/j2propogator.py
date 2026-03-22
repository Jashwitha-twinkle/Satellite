import numpy as np
from physics.constants import MU, RE, J2

def acceleration_j2(r):

    x, y, z = r
    r_norm = np.linalg.norm(r)

    factor = 1.5 * J2 * MU * RE**2 / r_norm**5

    ax = factor * x * (5*z**2/r_norm**2 - 1)
    ay = factor * y * (5*z**2/r_norm**2 - 1)
    az = factor * z * (5*z**2/r_norm**2 - 3)

    return np.array([ax, ay, az])


import numpy as np

def acceleration_total(r):

    r = np.array(r, dtype=float)   

    r_norm = np.linalg.norm(r)

    if r_norm == 0:
        return np.zeros(3)

    a_gravity = -MU * r / r_norm**3

    return a_gravity + acceleration_j2(r)