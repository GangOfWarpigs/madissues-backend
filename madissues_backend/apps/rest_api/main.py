import uvicorn
from fastapi import FastAPI
from madissues_backend.apps.rest_api.v1.owners import router as owners_router
from madissues_backend.apps.rest_api.v1.organizations import router as organizations_router

app = FastAPI()

app.include_router(owners_router)
app.include_router(organizations_router)

uvicorn.run(app)