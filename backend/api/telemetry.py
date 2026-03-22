from fastapi import APIRouter
from state.objects import update_object, get_objects
from conjuction.detection import detect_future_conjunctions


router = APIRouter()

@router.post("/api/telemetry")
def telemetry(data: dict):

    count = 0

    for obj in data["objects"]:

        state = [
            obj["r"]["x"],
            obj["r"]["y"],
            obj["r"]["z"],
            obj["v"]["x"],
            obj["v"]["y"],
            obj["v"]["z"]
        ]

        update_object(obj["id"], state, obj["type"])
        count += 1

    objects = get_objects()

    # pass only state vectors to conjunction detector
    state_map = {k: v["state"] for k, v in objects.items()}

    alerts = detect_future_conjunctions(state_map)

    return {
        "status": "ACK",
        "processed_count": count,
        "active_cdm_warnings": len(alerts)
    }