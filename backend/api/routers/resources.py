from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth import get_active_user
from ..actions import resources

router = APIRouter()

@router.get("/images/")
def get_images():
    return resources.get_images()

@router.get("/images/{image_id}")
def get_image(image_id):
    return resources.get_image(image_id)

@router.get("/images/{image_id}/pull")
def pull_image(image_id):
    return resources.update_image(image_id)

@router.delete("/images/{image_id}")
def delete_image(image_id):
    return resources.delete_image(image_id)