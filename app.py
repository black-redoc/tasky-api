import os
from typing import Annotated
import json
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

if os.getenv("ENVIRONMENT") == "development":
    load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

from fastapi import Cookie, FastAPI, HTTPException, Response, Request, status

from contextlib import asynccontextmanager

from src.tasks.router import router as task_router
from src.tasks import models as tasks_model
from src.projects.router import router as project_router
from src.projects import models as projects_model
from src.users.router import router as users_router
from src.users import models as users_model
from src.settings.database import create_database


from src.settings.database import SessionLocal, engine

allow_origins = os.getenv("ORIGINS")
allow_origins = allow_origins.split(",")
allow_methods = ("*",)
allow_headers = ("*",)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
    allow_credentials=True,
    expose_headers=("*",),
)


@app.get("/healthcheck")
def health():
    return "OK"


@app.get("/protected")
def protected(session: Annotated[str | None, Cookie()] = None):
    print("protected route")
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    user_data = json.loads(session)
    user_data = dict(email=user_data["email"])
    return JSONResponse(status_code=status.HTTP_200_OK, content=user_data)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except Exception:
        response = Response(
            "Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        request.state.db.close()
    return response


@app.middleware("http")
async def http_session_middleware(request: Request, call_next):
    if request.url.path in ["/healthcheck",]:
        return await call_next(request)
    try:
        origin = request.headers["Origin"]
        if origin not in allow_origins:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        response = await call_next(request)
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
    except HTTPException as e:
        response = JSONResponse(
            {"detail": e.detail}, status_code=e.status_code
        )
    except Exception as e:
        response = Response(
            f"Internal server error: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


app.include_router(task_router)
app.include_router(project_router)
app.include_router(users_router)
