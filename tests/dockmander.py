import docker

class dockmander():
    def __init__(self):
        self.client = docker.from_env()

    def run_container(self):
        self.client.containers.run(
            name = 'test',
            image = 'hello-world:latest',
            devices = [ '/:/home/user/Music' ],
            environment = ["PUID=1000", "PGID=100"],
            ports = {"4040":"4040/tcp"},
            restart_policy = {"Name": 'unless-stopped'}
        )
    def list_containers(self):
        self.client.containers.list(all=True)
        
dockmander1 = dockmander()

dockmander1.run_container()
dockmander1.list_containers()