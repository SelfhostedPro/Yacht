from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth import get_active_user
from ..actions import resources
from ..db.schemas.resources import ImageWrite, VolumeWrite, NetworkWrite
import netifaces


router = APIRouter()
### Images ###
@router.get("/images/", dependencies=[Depends(get_active_user)])
def get_images():
    return resources.get_images()

@router.post("/images/", dependencies=[Depends(get_active_user)])
def write_image(image: ImageWrite):
    return resources.write_image(image.image)

@router.get("/images/{image_id}", dependencies=[Depends(get_active_user)])
def get_image(image_id):
    return resources.get_image(image_id)

@router.get("/images/{image_id}/pull", dependencies=[Depends(get_active_user)])
def pull_image(image_id):
    return resources.update_image(image_id)

@router.delete("/images/{image_id}", dependencies=[Depends(get_active_user)])
def delete_image(image_id):
    return resources.delete_image(image_id)

### Volumes ###
@router.get("/volumes/", dependencies=[Depends(get_active_user)])
def get_volumes():
    return resources.get_volumes()

@router.post("/volumes/", dependencies=[Depends(get_active_user)])
def write_volume(name: VolumeWrite):
    return resources.write_volume(name.name)

@router.get("/volumes/{volume_name}", dependencies=[Depends(get_active_user)])
def get_volume(volume_name):
    return resources.get_volume(volume_name)

@router.delete("/volumes/{volume_name}", dependencies=[Depends(get_active_user)])
def delete_volume(volume_name):
    return resources.delete_volume(volume_name)

### Networks ###
@router.get("/networks/", dependencies=[Depends(get_active_user)])
def get_networks():
    return resources.get_networks()

@router.post("/networks/", dependencies=[Depends(get_active_user)])
def write_network(form: NetworkWrite):
    return resources.write_network(form)

@router.get("/networks/{network_name}", dependencies=[Depends(get_active_user)])
def get_network(network_name):
    return resources.get_network(network_name)

@router.delete("/networks/{network_name}", dependencies=[Depends(get_active_user)])
def delete_network(network_name):
    return resources.delete_network(network_name)
