from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def fakelogin():
    return {"email": "admin@yacht.local", "authDisabled": True}


@router.get("/check")
def auth_check():
    return {"email": "admin@yacht.local", "authDisabled": True}