from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from typing import List

from sqlalchemy.orm import Session
from datetime import datetime

from ..db import crud, schemas
from ..db.models import containers
from ..db.database import SessionLocal, engine
from ..utils.auth import get_db
from ..auth import get_active_user
from ..actions import apps
from ..actions import resources
from ..settings import Settings
import yaml

containers.Base.metadata.create_all(bind=engine)

settings = Settings()

router = APIRouter()


@router.get(
    "/variables",
    response_model=List[schemas.TemplateVariables],
    dependencies=[Depends(get_active_user)],
)
def read_template_variables(db: Session = Depends(get_db)):
    return crud.read_template_variables(db=db)


@router.post(
    "/variables",
    response_model=List[schemas.TemplateVariables],
    dependencies=[Depends(get_active_user)],
)
def set_template_variables(
    new_variables: List[schemas.TemplateVariables], db: Session = Depends(get_db)
):
    return crud.set_template_variables(new_variables=new_variables, db=db)


@router.get(
    "/export",
    response_model=schemas.Import_Export,
    dependencies=[Depends(get_active_user)],
)
def export_settings(db: Session = Depends(get_db)):
    return crud.export_settings(db=db)


@router.post("/export", dependencies=[Depends(get_active_user)])
def import_settings(db: Session = Depends(get_db), upload: UploadFile = File(...)):
    return crud.import_settings(db=db, upload=upload)


@router.get("/prune/{resource}", dependencies=[Depends(get_active_user)])
def prune_resources(resource: str):
    return resources.prune_resources(resource)


@router.get("/update", dependencies=[Depends(get_active_user)])
def update_self():
    return apps.update_self()


@router.get("/check/update", dependencies=[Depends(get_active_user)])
def check_self_update():
    return apps.check_self_update()
