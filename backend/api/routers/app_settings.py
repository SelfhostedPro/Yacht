from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from typing import List

from sqlalchemy.orm import Session
from datetime import datetime

from ..db import crud, schemas
from ..db.models import containers
from ..db.database import SessionLocal, engine
from ..utils.auth import get_db
from ..actions.apps import update_self, check_self_update
from ..actions import resources
from ..settings import Settings
import yaml
from fastapi_jwt_auth import AuthJWT

containers.Base.metadata.create_all(bind=engine)

settings = Settings()

router = APIRouter()


@router.get(
    "/variables",
    response_model=List[schemas.TemplateVariables],
    
)
def read_template_variables(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return crud.read_template_variables(db=db)


@router.post(
    "/variables",
    response_model=List[schemas.TemplateVariables],
    
)
def set_template_variables(
    new_variables: List[schemas.TemplateVariables], db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return crud.set_template_variables(new_variables=new_variables, db=db)


@router.get(
    "/export",
    response_model=schemas.Import_Export,
    
)
def export_settings(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return crud.export_settings(db=db)


@router.post("/export", )
def import_settings(db: Session = Depends(get_db), upload: UploadFile = File(...), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return crud.import_settings(db=db, upload=upload)


@router.get("/prune/{resource}", )
def prune_resources(resource: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return resources.prune_resources(resource)


@router.get("/update", )
def update_self(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return update_self()


@router.get("/check/update", )
def _check_self_update(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return check_self_update()
