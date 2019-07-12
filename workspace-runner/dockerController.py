import docker

client = docker.from_env()

def createContainer():

    placaeholder = client.containers.run("jupyterlab-workspace:latest", 
        auto_remove=False, detach = True)

    return True

def getContainers():
    containerList = client.containers.list()

    return containerList