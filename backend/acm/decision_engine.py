import numpy as np

from acm.evasion_solver import compute_evasion_delta_v
from acm.risk_model import compute_collision_risk


def autonomous_maneuver_planner(alerts, objects, current_time):

    maneuvers = []

    for alert in alerts:

        sat1 = alert["sat1"]
        sat2 = alert["sat2"]

        tca = alert["tca_seconds"]
        miss = alert["miss_distance_km"]

        risk = compute_collision_risk(tca, miss)

        # Only react to high-risk conjunctions
        if risk != "HIGH":
            continue

        # Safety check
        if sat1 not in objects or sat2 not in objects:
            continue

        s1 = objects[sat1]["state"]
        s2 = objects[sat2]["state"]

        r1 = np.array(s1[:3])
        v1 = np.array(s1[3:])

        r2 = np.array(s2[:3])
        v2 = np.array(s2[3:])

        dv = compute_evasion_delta_v(r1, v1, r2, v2)

        # ⭐ Define evasion burn
        burn1 = {
            "burn_id": f"EVASION_{sat1}_{sat2}",
            "burnTime": current_time + 60,
            "deltaV_vector": {
                "x": float(dv[0]),
                "y": float(dv[1]),
                "z": float(dv[2])
            }
        }

        # ⭐ Recovery burn
        burn2 = {
            "burn_id": f"RECOVERY_{sat1}_{sat2}",
            "burnTime": current_time + 600,
            "deltaV_vector": {
                "x": float(-dv[0]),
                "y": float(-dv[1]),
                "z": float(-dv[2])
            }
        }

        maneuver = {
            "satelliteId": sat1,
            "maneuver_sequence": [
                burn1,
                burn2
            ]
        }

        maneuvers.append(maneuver)

    return maneuvers