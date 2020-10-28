from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth import get_active_user
from ..actions.compose import get_compose_projects, compose_action, get_compose

router = APIRouter()

@router.get("/")
def get_projects():
    return get_compose_projects()

@router.get("/{project_name}")
def get_project(project_name):
    return get_compose(project_name)

@router.get("/{project_name}/{action}")
def get_compose_action(project_name, action):
    return compose_action(project_name, action)