from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

# In-memory storage
incidents = []
incident_counter = 1


# Health check
@app.get("/")
def home():
    return {"message": "IMS Project Running"}


# Receive signal
@app.post("/signal")
def receive_signal(signal: dict):
    global incident_counter

    component = signal.get("component")
    error = signal.get("error")
    now = datetime.now()

    signal["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")

    # Check existing incidents
    for incident in incidents:
        incident_time = datetime.strptime(
            incident["created_at"], "%Y-%m-%d %H:%M:%S"
        )

        if (
            incident["component"] == component
            and incident["status"] == "OPEN"
            and (now - incident_time) <= timedelta(seconds=10)
        ):
            incident["signals"].append(signal)
            return {
                "message": "Added to existing incident",
                "incident": incident
            }

    # Create new incident
    new_incident = {
        "id": incident_counter,
        "component": component,
        "status": "OPEN",
        "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "signals": [signal]
    }

    incidents.append(new_incident)
    incident_counter += 1

    return {
        "message": "New incident created",
        "incident": new_incident
    }


# Get all incidents
@app.get("/incidents")
def get_incidents():
    return incidents


# Close incident + RCA + MTTR
@app.post("/close/{id}")
def close_incident(id: int, rca: dict):
    for incident in incidents:
        if incident["id"] == id:

            if not rca:
                return {"error": "RCA is required"}

            closed_time = datetime.now()
            created_time = datetime.strptime(
                incident["created_at"], "%Y-%m-%d %H:%M:%S"
            )

            mttr = (closed_time - created_time).total_seconds()

            incident["status"] = "CLOSED"
            incident["rca"] = rca
            incident["closed_at"] = closed_time.strftime("%Y-%m-%d %H:%M:%S")
            incident["mttr_seconds"] = mttr

            return {
                "message": "Incident closed",
                "incident": incident
            }

    return {"error": "Incident not found"}
