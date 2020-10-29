from ..auth import cookie_authentication
from ..auth import user_db
from ..settings import Settings
from ..db.database import SessionLocal
from fastapi import WebSocket

settings = Settings()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def websocket_auth(websocket: WebSocket):
    try:
        cookie = websocket._cookies["fastapiusersauth"]
        user = await cookie_authentication(cookie, user_db)
        if user and user.is_active:
            return user
        elif settings.DISABLE_AUTH == "True":
            return True
    except:
        if settings.DISABLE_AUTH == "True":
            return True
        else:
            return None