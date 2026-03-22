from fastapi import FastAPI

from api.telemetry import router as telemetry_router
from api.maneuver import router as maneuver_router
from api.simulate import router as simulation_router
from api.visualization import router as visualization_router

app = FastAPI()

app.include_router(telemetry_router)
app.include_router(maneuver_router)
app.include_router(simulation_router)
app.include_router(visualization_router)