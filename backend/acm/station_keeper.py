import numpy as np

DRIFT_LIMIT = 10.0   # km


def check_station_keeping(objects, dt):

    outages = 0

    for sat_id, sat in objects.items():

        if sat["type"] != "SATELLITE":
            continue

        current_pos = np.array(
            sat["state"][:3]
        )

        slot_pos = np.array(
            sat["slot_position"]
        )

        drift = np.linalg.norm(
            current_pos - slot_pos
        )

        # -------------------------
        # OUTSIDE BOX
        # -------------------------

        if drift > DRIFT_LIMIT:

            sat["outage_seconds"] += dt

            outages += 1

        else:

            # inside slot
            sat["outage_seconds"] = 0

    return outages