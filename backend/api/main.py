import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException
from .routers import apps, templates, app_settings
import uuid

from .db import models
from .db.database import SessionLocal
from .routers.app_settings import read_template_variables, set_template_variables, SessionLocal
from sqlalchemy.orm import Session

from .settings import Settings
from .utils import get_db

from .auth import fastapi_users, cookie_authentication, database, users, user_create, UserDB, get_password_hash

app = FastAPI(root_path="/api")
settings = Settings()

app.include_router(
    apps.router,
    prefix="/apps",
    tags=["apps"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    fastapi_users.get_auth_router(cookie_authentication),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"]
)
app.include_router(
    templates.router,
    prefix="/templates",
    tags=["templates"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    app_settings.router,
    prefix="/settings",
    tags=["settings"]
)
@app.on_event("startup")
async def startup():
    await database.connect()
    users_exist = await database.fetch_all(query=users.select())
    if users_exist:
        print("users exist")
    else:
        print("no users")
        ### This is where I'm having trouble
        hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
        base_user = UserDB(
            id = uuid.uuid4(),
            email = settings.ADMIN_EMAIL,
            hashed_password = hashed_password,
            is_active = True,
            is_superuser = True
        )
        user_created = await user_create(base_user)
    template_variables_exist = read_template_variables(SessionLocal())
    if template_variables_exist:
        print("template variables exist")
    else:
        print("No Variables yet!")
        t_vars = settings.BASE_TEMPLATE_VARIABLES
        t_var_list = []
        for t in t_vars:
            template_variables = models.TemplateVariables(
                variable=t.get("variable"),
                replacement=t.get("replacement")
            )
            t_var_list.append(template_variables)
        set_template_variables(new_variables=t_var_list, db=SessionLocal())
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
