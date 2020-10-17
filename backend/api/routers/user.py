from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
def fakelogin():
    return {"email": "admin@yacht.local", "authDisabled": True}