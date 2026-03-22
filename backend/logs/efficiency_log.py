efficiency_log = []


def log_efficiency(
    current_time,
    fuel_used,
    collisions_avoided
):

    efficiency_log.append({
        "time": current_time,
        "fuel_used": fuel_used,
        "collisions_avoided": collisions_avoided
    })


def get_efficiency_data():

    return efficiency_log