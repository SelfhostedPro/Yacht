from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from ..db import models, crud, schemas, database
from sqlalchemy.orm import Session
from ..utils import get_db
from ..auth import auth_check
from ..settings import Settings

router = APIRouter()
settings = Settings()


@router.post("/create", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    auth_check(Authorize)
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already in use")
    return crud.create_user(db=db, user=user)


@router.post("/login")
def login(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    _user = db.query(models.User).filter(models.User.username == user.username).first()
    if _user is not None and crud.verify_password(user.password, _user.hashed_password):
        # Create Tokens
        access_token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)

        # Assign cookies
        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)
        return {
            "login": "successful",
            "username": _user.username,
            "access_token": access_token,
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid Username or Password.")


@router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)
    return {"refresh": "successful", "access_token": new_access_token}


@router.get("/me", response_model=schemas.User)
def get_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    auth_check(Authorize)
    if settings.DISABLE_AUTH == "True":
        current_user = models.User
        current_user.authDisabled = True
        current_user.id = 0
        current_user.username = "user"
        current_user.is_active = True
        current_user.is_superuser = True
        return current_user
    else:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        if current_user != None:
            return crud.get_user_by_name(db=db, username=current_user)
        else:
            raise HTTPException(status_code=401, detail="Not logged in.")


@router.post("/me", response_model=schemas.User)
def update_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    auth_check(Authorize)
    current_user = Authorize.get_jwt_subject()
    return crud.update_user(db=db, user=user, current_user=current_user)


@router.get("/logout")
def logout(Authorize: AuthJWT = Depends()):
    auth_check(Authorize)
    Authorize.unset_jwt_cookies()
    return {"msg": "Logout Successful"}
