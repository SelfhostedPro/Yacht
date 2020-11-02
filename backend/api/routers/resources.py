from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..actions import resources
from ..db.schemas.resources import ImageWrite, VolumeWrite, NetworkWrite


router = APIRouter()
### Images ###
@router.get("/images/", )
def get_images():
    return resources.get_images()


@router.post("/images/", )
def write_image(image: ImageWrite):
    return resources.write_image(image.image)


@router.get("/images/{image_id}", )
def get_image(image_id):
    return resources.get_image(image_id)


@router.get("/images/{image_id}/pull", )
def pull_image(image_id):
    return resources.update_image(image_id)


@router.delete("/images/{image_id}", )
def delete_image(image_id):
    return resources.delete_image(image_id)


### Volumes ###
@router.get("/volumes/", )
def get_volumes():
    return resources.get_volumes()


@router.post("/volumes/", )
def write_volume(name: VolumeWrite):
    return resources.write_volume(name.name)


@router.get("/volumes/{volume_name}", )
def get_volume(volume_name):
    return resources.get_volume(volume_name)


@router.delete("/volumes/{volume_name}", )
def delete_volume(volume_name):
    return resources.delete_volume(volume_name)


### Networks ###
@router.get("/networks/", )
def get_networks():
    return resources.get_networks()


@router.post("/networks/", )
def write_network(form: NetworkWrite):
    return resources.write_network(form)


@router.get("/networks/{network_name}", )
def get_network(network_name):
    return resources.get_network(network_name)


@router.delete("/networks/{network_name}", )
def delete_network(network_name):
    return resources.delete_network(network_name)
