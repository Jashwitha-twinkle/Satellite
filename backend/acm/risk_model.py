def compute_collision_risk(tca, miss_distance):

    if miss_distance < 0.5:
        return "HIGH"

    if miss_distance < 0.2:
        return "MEDIUM"

    return "LOW"