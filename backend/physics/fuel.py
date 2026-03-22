import numpy as np

Isp = 300.0
g0 = 9.80665

def fuel_required(mass, dv):

    dv_mag = np.linalg.norm(dv) * 1000  # km/s → m/s

    delta_m = mass * (1 - np.exp(-dv_mag / (Isp * g0)))

    return delta_m