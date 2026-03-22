outage_log = []


def log_outage(
    current_time,
    outages
):

    outage_log.append({
        "time": current_time,
        "active_outages": outages
    })


def get_outage_history():

    return outage_log