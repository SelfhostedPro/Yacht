import docker

class Dockmander():
    def __init__(self):
        self.client = docker.from_env

    def init_app(self, app):
        self.app = app 

    def setup_container(self, *args, **kwargs):
        container = client.containers.run(
            name=name,
            image=image,
            devices=devices,
            environment=env,
            ports=ports,
            restart_policy=restart_policy,
            volumes=volumes
            )