import numpy as np

from acm.rtn_frame import compute_rtn_frame
from acm.rtn_frame import rtn_to_eci


def compute_evasion_delta_v(r1, v1, r2, v2):

    # relative vectors
    r_rel = r2 - r1
    v_rel = v2 - v1

    # build RTN frame
    r_hat, t_hat, n_hat = compute_rtn_frame(r1, v1)

    # -------------------------
    # Primary: Transverse burn
    # -------------------------

    # Determine if closing speed is high
    closing_speed = np.dot(r_rel, v_rel)

    if closing_speed < 0:
        dv_t = 0.002   # km/s
    else:
        dv_t = -0.002

    # -------------------------
    # Small radial adjustment
    # -------------------------

    dv_r = 0.0005 * np.sign(np.dot(r_rel, r_hat))

    # -------------------------
    # Minimal normal component
    # -------------------------

    dv_n = 0.0001   # very small


    # RTN vector
    dv_rtn = np.array([
        dv_r,
        dv_t,
        dv_n
    ])


    # Convert RTN → ECI
    dv_eci = rtn_to_eci(
        dv_rtn,
        r1,
        v1
    )

    return dv_eci