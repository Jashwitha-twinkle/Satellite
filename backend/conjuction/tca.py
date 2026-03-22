import numpy as np

def compute_tca(r1, v1, r2, v2):

    r = np.array(r2) - np.array(r1)
    v = np.array(v2) - np.array(v1)

    v_norm_sq = np.dot(v, v)

    if v_norm_sq == 0:
        return None, np.linalg.norm(r)

    tca = -np.dot(r, v) / v_norm_sq

    closest_vector = r + v * tca
    miss_distance = np.linalg.norm(closest_vector)

    return tca, miss_distance