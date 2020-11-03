import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException
from .routers import apps, templates, app_settings, resources, auth, user, compose
import uuid

from .db import models
from .db.database import SessionLocal, engine
from .routers.app_settings import (
    read_template_variables,
    set_template_variables,
    SessionLocal,
)
from backend.api.db.schemas.templates import TemplateBase
from backend.api.db.crud.templates import (
    get_templates,
    add_template
)
from sqlalchemy.orm import Session

from .settings import Settings
from .utils import get_db

from .auth import (
    fastapi_users,
    cookie_authentication,
    database,
    users,
    user_create,
    UserDB,
    get_password_hash,
)

app = FastAPI(root_path="/api")

models.Base.metadata.create_all(bind=engine)

settings = Settings()

print(settings.DISABLE_AUTH)

app.include_router(
    apps.router,
    prefix="/apps",
    tags=["apps"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    resources.router, prefix="/resources", tags=["resources"],
)
if settings.DISABLE_AUTH == "True":
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
else:
    app.include_router(
        fastapi_users.get_auth_router(cookie_authentication),
        prefix="/auth",
        tags=["auth"],
    )
if settings.DISABLE_AUTH == "True":
    app.include_router(user.router, prefix="/users", tags=["users"])
else:
    app.include_router(
        fastapi_users.get_users_router(), prefix="/users", tags=["users"]
    )
app.include_router(
    templates.router,
    prefix="/templates",
    tags=["templates"],
    responses={404: {"description": "Not found"}},
)
app.include_router(compose.router, prefix="/compose", tags=["compose"])
app.include_router(app_settings.router, prefix="/settings", tags=["settings"])


@app.on_event("startup")
async def startup():
    await database.connect()
    # Clear old db migrations
    delete_alembic = "DROP TABLE IF EXISTS alembic_version;"
    await database.execute(delete_alembic)
    users_exist = await database.fetch_all(query=users.select())
    if users_exist:
        print("Users Exist")
    else:
        print("No Users. Creating the default user.")
        # This is where I'm having trouble
        hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
        base_user = UserDB(
            id=uuid.uuid4(),
            email=settings.ADMIN_EMAIL,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=True,
        )
        user_created = await user_create(base_user)

    existing_templates = get_templates(SessionLocal())
    if hasattr(settings, 'BASE_TEMPLATE'):
        base_template_url = settings.BASE_TEMPLATE
        if base_template_url:
            for _template in existing_templates:
                if base_template_url in _template.url:
                    base_exists = True
                    break
            else:
                base_exists = False
            if base_exists == False:
                add_template(SessionLocal(), template=TemplateBase(title='default', url= base_template_url))

    template_variables_exist = read_template_variables(SessionLocal())
    if template_variables_exist:
        print("Template Variables Exist")
    else:
        print("No Variables yet!")
        t_vars = settings.BASE_TEMPLATE_VARIABLES
        t_var_list = []
        for t in t_vars:
            template_variables = models.TemplateVariables(
                variable=t.get("variable"), replacement=t.get("replacement")
            )
            t_var_list.append(template_variables)
        set_template_variables(new_variables=t_var_list, db=SessionLocal())


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
