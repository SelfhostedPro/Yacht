from fastapi import FastAPI
from pydantic import BaseModel

class ImageWrite(BaseModel):
    image: str

class VolumeWrite(BaseModel):
    name: str