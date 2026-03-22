import numpy as np


def compute_rtn_frame(r, v):

    r_hat = r / np.linalg.norm(r)

    v_hat = v / np.linalg.norm(v)

    n_hat = np.cross(r_hat, v_hat)
    n_hat = n_hat / np.linalg.norm(n_hat)

    t_hat = np.cross(n_hat, r_hat)

    return r_hat, t_hat, n_hat


def rtn_to_eci(dv_rtn, r, v):

    dv_r, dv_t, dv_n = dv_rtn

    r_hat, t_hat, n_hat = compute_rtn_frame(r, v)

    dv_eci = (
        dv_r * r_hat +
        dv_t * t_hat +
        dv_n * n_hat
    )

    return dv_eci