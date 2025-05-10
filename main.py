from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.db import create_all_tables
from app.routers import clients, transactions, misc, suscriptions

app = FastAPI(lifespan=create_all_tables)

# Include the routers
app.include_router(clients.router)
app.include_router(transactions.router)
app.include_router(suscriptions.router)
# app.include_router(misc.router)

security = HTTPBasic()

@app.get("/")
async def root(credencials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"message": "Welcome to the API"}

