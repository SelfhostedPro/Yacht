from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth import get_active_user
from ..actions.compose import get_compose_projects, compose_action

router = APIRouter()

@router.get("/")
def get_images():
    return get_compose_projects()

@router.get("/{project_name}/{action}")
def actions(project_name, action):
    return compose_action(project_name, action)