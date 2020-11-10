import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from .routers import apps, templates, app_settings, resources, compose, users
import uuid

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db.crud.templates import (
    read_template_variables,
    set_template_variables,
)
from .settings import Settings

from .utils import get_db

from .db.crud import create_user, get_users
from .db.models import User, TemplateVariables
from .db.database import SessionLocal
from .db.schemas import UserCreate

app = FastAPI(root_path="/api")

settings = Settings()


class jwtSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_token_location: set = {"headers", "cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_samesite: str = "lax"


@AuthJWT.load_config
def get_config():
    return jwtSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(users.router, prefix="/auth", tags=["users"])
app.include_router(apps.router, prefix="/apps", tags=["apps"])
app.include_router(
    resources.router, prefix="/resources", tags=["resources"],
)
app.include_router(
    templates.router, prefix="/templates", tags=["templates"],
)
app.include_router(compose.router, prefix="/compose", tags=["compose"])
app.include_router(app_settings.router, prefix="/settings", tags=["settings"])


@app.on_event("startup")
async def startup(db: Session = Depends(get_db)):
    # await database.connect()
    # Clear old db migrations
    delete_alembic = "DROP TABLE IF EXISTS alembic_version;"
    # await database.execute(delete_alembic)
    users_exist = get_users(db=SessionLocal())
    if users_exist:
        print("Users Exist")
    else:
        print("No Users. Creating the default user.")
        # This is where I'm having trouble
        user = UserCreate(
            username=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD
        )
        create_user(db=SessionLocal(), user=user)
    template_variables_exist = read_template_variables(SessionLocal())
    if template_variables_exist:
        print("Template Variables Exist")
    else:
        print("No Variables yet!")
        t_vars = settings.BASE_TEMPLATE_VARIABLES
        t_var_list = []
        for t in t_vars:
            template_variables = TemplateVariables(
                variable=t.get("variable"), replacement=t.get("replacement")
            )
            t_var_list.append(template_variables)
        set_template_variables(new_variables=t_var_list, db=SessionLocal())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
