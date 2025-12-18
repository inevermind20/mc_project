from fastapi import FastAPI
from api import clients, equipments, proposals, assistances, calendar
from auth import auth_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(clients.router, prefix="/clients")
app.include_router(equipments.router, prefix="/equipments")
app.include_router(proposals.router, prefix="/proposals")
app.include_router(assistances.router, prefix="/assistances")
app.include_router(calendar.router, prefix="/calendar")
