from fastapi import APIRouter, Depends, HTTPException, WebSocket, status, Cookie
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import make_transient

from ..db import models, schemas
from ..db.models import containers
from ..db.database import SessionLocal, engine
from .. import actions
from ..auth import get_active_user, User
from ..utils import websocket_auth, calculate_blkio_bytes, calculate_cpu_percent, calculate_cpu_percent2, calculate_network_bytes, get_app_stats

import docker
import aiodocker
from datetime import datetime
import urllib.request
import json

containers.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", dependencies=[Depends(get_active_user)])
def index():
    return actions.get_apps()


@router.get("/{app_name}", dependencies=[Depends(get_active_user)])
def get_container_details(app_name):
    return actions.get_app(app_name=app_name)


@router.get("/{app_name}/processes", response_model=schemas.Processes, dependencies=[Depends(get_active_user)])
def get_container_processes(app_name):
    return actions.get_app_processes(app_name=app_name)


@router.get("/{app_name}/logs", response_model=schemas.AppLogs, dependencies=[Depends(get_active_user)])
def get_container_logs(app_name):
    return actions.get_app_logs(app_name=app_name)


@router.get("/{app_name}/{action}", dependencies=[Depends(get_active_user)])
def container_actions(app_name, action):
    return actions.app_action(app_name, action)


@router.post("/deploy", response_model=schemas.DeployLogs, dependencies=[Depends(get_active_user)])
def deploy_app(template: schemas.DeployForm):
    return actions.deploy_app(template=template)


@router.websocket("/{app_name}/livelogs")
async def logs(websocket: WebSocket, app_name: str):

    auth_success = await websocket_auth(websocket=websocket)
    if auth_success:
        await websocket.accept()
        async with aiodocker.Docker() as docker:
            container: DockerContainer = await docker.containers.get(app_name)
            logs = container.log(stdout=True, stderr=True, follow=True)
            async for line in logs:
                try:
                    await websocket.send_text(line)
                except Exception as e:
                    return e
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)


@router.websocket("/{app_name}/stats")
async def stats(websocket: WebSocket, app_name: str):

    auth_success = await websocket_auth(websocket=websocket)
    if auth_success:
        await websocket.accept()
        async with aiodocker.Docker() as docker:
            cpu_total = 0.0
            cpu_system = 0.0
            cpu_percent = 0.0

            container: DockerContainer = await docker.containers.get(app_name)
            stats = container.stats(stream=True)
            async for line in stats:
                mem_current = line["memory_stats"]["usage"]
                mem_total = line["memory_stats"]["limit"]

                try:
                    cpu_percent, cpu_system, cpu_total = await calculate_cpu_percent2(line, cpu_total, cpu_system)
                except KeyError as e:
                    print("error while getting new CPU stats: %r, falling back")
                    cpu_percent = await calculate_cpu_percent(line)

                full_stats = {
                    "time": line['read'],
                    "cpu_percent": cpu_percent,
                    "mem_current": mem_current,
                    "mem_total": line["memory_stats"]["limit"],
                    "mem_percent": (mem_current / mem_total) * 100.0,
                }
                try:
                    await websocket.send_text(json.dumps(full_stats))
                except Exception as e:
                    return e
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)