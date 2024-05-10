import os

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles

from madissues_backend.apps.rest_api.v1.owners import router as owners_router
from madissues_backend.apps.rest_api.v1.organizations import router as organizations_router
from madissues_backend.apps.rest_api.v1.students import router as students_router
from madissues_backend.apps.rest_api.v1.task_manager import router as task_manager_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5734",
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dirname = os.path.dirname(__file__)

app.mount("/public",
          StaticFiles(directory=os.path.join(dirname, "assets")),
          name="static")
app.include_router(owners_router)
app.include_router(organizations_router)
app.include_router(students_router)
app.include_router(task_manager_router)
