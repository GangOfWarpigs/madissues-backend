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
from madissues_backend.apps.rest_api.v1.issues import router as issues_manager_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5734",
    "*"
]

description = """
The **Madissues Rest API** leverages Domain-Driven Design (DDD) within a Vertical Slice Architecture to manage educational ecosystems across five main subdomains: owners, organizations, students, task manager, and issues. This structure ensures that each aspect of the educational framework is addressed efficiently and comprehensively.

### Owners Subdomain
Handles all owner-related functionalities, including account creation, login, email updates, and profile management. This subdomain facilitates administrative control and personal account management for educational administrators.

### Organizations Subdomain
Central to setting up and managing educational structures, it offers endpoints for creating organizations, adding courses, enrolling teachers, and establishing degree programs. This enhances organizational flexibility and educational offerings management.

### Students Subdomain
Focuses on student interactions with the system, providing endpoints for registration, login, personal and profile updates, and sensitive operations like account bans or deletions. It ensures responsive student management tailored to individual and administrative needs.

### Task Manager and Issues Subdomains
Integrate additional functionalities for organizational efficiency. The Task Manager subdomain allows integration with task management systems, facilitating better academic and administrative task coordination. The Issues subdomain enables issue creation and management, promoting prompt problem resolution and continuous system improvement.

"""

tags_metadata = [
    {
        "name": "owners",
        "description": "Operations with owners. The **login** and **account management** logic is also here.",
    },
    {
        "name": "students",
        "description": "Manage student accounts and preferences.",
    },
    {
        "name": "organizations",
        "description": "Operations related to organizations, courses, teachers, and degrees. This subdomain enables comprehensive management of educational structures.",
    },
    {
        "name": "task manager",
        "description": "Integration and management of task-related functionalities within organizations.",
        "externalDocs": {
            "description": "Explore task management trello integration",
            "url": "https://developer.atlassian.com/cloud/trello/rest/api-group-actions/#api-group-actions",
        },
    },
    {
        "name": "issues",
        "description": "Handle creation and management of issues to ensure robust problem resolution and system feedback.",
    },
]

app = FastAPI(
    title="Madissues REST API",
    description=description,
    summary="This is madissues rest api for integrations",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dirname = os.path.dirname(__file__)
dirname = os.path.abspath(os.path.join(dirname, '../../../'))

app.mount("/media",
          StaticFiles(directory=os.path.join(dirname, "madissues_backend", "media")),
          name="media")
app.include_router(owners_router)
app.include_router(organizations_router)
app.include_router(students_router)
app.include_router(task_manager_router)
app.include_router(issues_manager_router)
