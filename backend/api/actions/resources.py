import docker
import json

def get_images():
    dclient = docker.from_env()
    containers = dclient.containers.list(all=True)
    images = dclient.images.list(all=True)
    image_list = []
    for image in images:
        attrs = image.attrs
        for container in containers:
            if container.image.id in image.id:
                attrs.update({'inUse': True})
        if attrs.get('inUse') == None:
            attrs.update({'inUse': False})

        image_list.append(attrs)
    return image_list

def get_image(image_id):
    dclient = docker.from_env()
    image = dclient.images.get(image_id)
    return image.attrs

def update_image(image_id):
    dclient = docker.from_env()
    image = dclient.images.get(image_id)
    new_image = dclient.images.get_registry_data(image.tags[0])
    new_image.pull()
    return get_image(image_id)

def delete_image(image_id):
    dclient = docker.from_env()
    image = dclient.images.get(image_id)
    dclient.images.remove(image_id, force=True)
    return image.attrs

def prune_resources(resource):
    dclient = docker.from_env()
    action = getattr(dclient, resource)
    if resource == 'images':
        deleted_resource = action.prune(filters={'dangling': False})
    else:
        deleted_resource = action.prune()
    return deleted_resource