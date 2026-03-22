import numpy as np
from conjuction.tca import compute_tca
from conjuction.spatial import SpatialIndex


def detect_future_conjunctions(objects):

    
    if len(objects) < 2:
        return []

    ids = list(objects.keys())

    
    positions = []
    valid_ids = []

    for obj_id in ids:

        state = objects[obj_id]

        # skip invalid or malformed states
        if state is None or len(state) < 6:
            continue

        positions.append(state[:3])
        valid_ids.append(obj_id)

    # 🚨 Guard 3: still need at least 2 valid objects
    if len(positions) < 2:
        return []

    # build KDTree
    index = SpatialIndex(positions)

    pairs = index.query_neighbors(radius=50)   # km search radius

    alerts = []

    for i, j in pairs:

        s1 = objects[valid_ids[i]]
        s2 = objects[valid_ids[j]]

        r1 = np.array(s1[:3])
        v1 = np.array(s1[3:])

        r2 = np.array(s2[:3])
        v2 = np.array(s2[3:])

        result = compute_tca(r1, v1, r2, v2)

        if result is None:
            continue

        tca, miss = result

        if tca is None:
            continue

        if 0 < tca < 86400 and miss < 0.1:

            alerts.append({
                "sat1": valid_ids[i],
                "sat2": valid_ids[j],
                "tca_seconds": float(tca),
                "miss_distance_km": float(miss)
            })

    return alerts