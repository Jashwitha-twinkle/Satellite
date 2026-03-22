fuel_history = {}


def log_fuel_state(objects, current_time):

    for sat_id, sat in objects.items():

        if sat["type"] != "SATELLITE":
            continue

        if sat_id not in fuel_history:
            fuel_history[sat_id] = []

        fuel_history[sat_id].append({
            "time": current_time,
            "fuel": sat["fuel"]
        })


def get_fuel_history():

    return fuel_history