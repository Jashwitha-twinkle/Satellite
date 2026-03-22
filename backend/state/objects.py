objects = {}
maneuvers = []

def update_object(obj_id, state, obj_type):

    if obj_id not in objects:

        objects[obj_id] = {
            "type": obj_type,
            "state": state,
            "fuel": 50.0,
            "mass": 550.0,
            "initial_fuel":50.0,
            "last_burn": -10000,
            "slot_position": state[:3].copy(),
            "outage_seconds": 0
        }

    else:
        objects[obj_id]["state"] = state


def get_objects():
    return objects


def add_maneuver(m):
    maneuvers.append(m)


def get_maneuvers():
    return maneuvers