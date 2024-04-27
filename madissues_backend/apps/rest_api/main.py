import uvicorn
from fastapi import FastAPI
from madissues_backend.apps.rest_api.v1.owners import router as owners_router

app = FastAPI()

app.include_router(owners_router)

uvicorn.run(app)