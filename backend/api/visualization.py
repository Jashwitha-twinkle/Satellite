from fastapi import APIRouter
from state.objects import get_objects

router = APIRouter()


@router.get("/api/visualization/snapshot")
def snapshot():

    objects = get_objects()

    satellites = []
    debris = []

    for obj_id, sat in objects.items():

        state = sat["state"]

        if sat["type"] == "SATELLITE":

            fuel = sat["fuel"]
            initial = sat["initial_fuel"]

            ratio = fuel / initial
            fuel_percent = (
                fuel / initial
            ) * 100
            # ⭐ status logic (INSIDE loop)
            if ratio <= 0.05:
                status = "EOL_PENDING"

            elif ratio <= 0.2:
                status = "LOW_FUEL"

            else:
                status = "NOMINAL"

            satellites.append({
                "id": obj_id,
                "lat": state[0],
                "lon": state[1],
                "fuel_kg": round(fuel, 2),
                "fuel_percent": round(fuel_percent, 1),
                "status": status
            })

        else:

            debris.append([
                obj_id,
                state[0],
                state[1],
                state[2]
            ])

    return {
        "timestamp": 0,
        "satellites": satellites,
        "debris_cloud": debris
    }

