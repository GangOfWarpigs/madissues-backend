import os

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles

from madissues_backend.apps.rest_api.v1.owners import router as owners_router
from madissues_backend.apps.rest_api.v1.organizations import router as organizations_router
from madissues_backend.apps.rest_api.v1.students import router as students_router

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Madissues API",
        version="2.5.0",
        summary="This is madissues OpenAPI documentation",
        description="Madissues is a service that allows students to complain easily about teachers and college issues",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "http://localhost:8000/public/logo.png"
    }
    openapi_schema["info"]["x-logo"]["backgroundColor"] = "#f5f5f5"

    app.openapi_schema = openapi_schema
    return app.openapi_schema


dirname = os.path.dirname(__file__)
app.mount("/public", StaticFiles(directory=os.path.join(dirname, "assets")), name="static")
app.include_router(owners_router)
app.include_router(organizations_router)
app.include_router(students_router)

app.openapi = custom_openapi
