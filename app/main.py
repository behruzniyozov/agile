from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from admin.settings import admin
from routers.auth import router as auth_router
from routers.projects import router as projects_router
from routers.tasks import router as tasks_router
from settings import MEDIA_DIR, MEDIA_URL

app = FastAPI()


@app.get("/")
async def hello():
    return {"detail": "Hello World!"}


app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="AGILE Task Management API",
        version="0.1.0",
        description="API with JWT-based Authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

admin.mount_to(app=app)
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_DIR), name=MEDIA_DIR)
