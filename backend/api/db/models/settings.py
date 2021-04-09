from sqlalchemy import (
    Column,
    String,
    Boolean
)
from api.db.database import Base


class SecretKey(Base):
    __tablename__ = "secret_key"
    key = Column(String, primary_key=True, index=True)


# class TokenBlacklist(Base):
#     __tablename__ = "jwt_token_blacklist"
#     jti = Column(String, primary_key=True, index=True)
#     expires = Column()
#     blacklisted = Column(String, nullable=False)
#     revoked = Column(String, nullable=False)
