import numpy as np

def check_eol_required(satellite):

    fuel = satellite["fuel"]

    initial_fuel = satellite.get("initial_fuel", 50.0)

    threshold = 0.05 * initial_fuel

    return fuel <= threshold


def compute_graveyard_delta_v(state):

    r = np.array(state[:3])
    v = np.array(state[3:])

    r_hat = r / np.linalg.norm(r)

    # small outward radial burn
    dv = 0.01 * r_hat   # km/s

    return dv


def schedule_eol_maneuver(objects, current_time):

    eol_maneuvers = []

    for sat_id, sat in objects.items():

        if sat["type"] != "SATELLITE":
            continue

        if not check_eol_required(sat):
            continue

        dv = compute_graveyard_delta_v(sat["state"])

        maneuver = {
            "satelliteId": sat_id,
            "maneuver_sequence": [
                {
                    "burn_id": f"EOL_{sat_id}",
                    "burnTime": current_time + 120,
                    "deltaV_vector": {
                        "x": float(dv[0]),
                        "y": float(dv[1]),
                        "z": float(dv[2])
                    }
                }
            ]
        }

        eol_maneuvers.append(maneuver)

    return eol_maneuvers