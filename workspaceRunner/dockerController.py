import docker
import utils
import time
from models import WorkSpaceContainer
from settings import defaultInternalPort

client = docker.from_env()

#TODO: organize container/template names by adding a template class, and associated functions 
def createContainer(containerType, username, projectName):

    randomPort = utils.randomPort()

    portSetting = {
       defaultInternalPort + "/tcp" : randomPort
    }

    if containerType == "jupyterLab":
        print("Starting JupyterLab Container...")
        container =  client.containers.run("jupyterlab-workspace:latest", 
            auto_remove=False, detach = True, ports=portSetting)

    elif containerType == "rStudio":
        print("Starting RStudio Container...")
        container = client.containers.run("rstudio-workspace:latest", 
            auto_remove=False, detach = True, ports=portSetting)

    waitForContainerStable(container)
    containerInstance = dictToContainerObj(container.__dict__['attrs'])

    return containerInstance

def getContainers():
    containerList = client.containers.list()
    fmtContainerList = []

    for container in containerList:

        fmtContainerList.append()
        fmtContainerList.append(ContainerObject(**container.__dict__['attrs']))

    return fmtContainerList

#TODO: Handle case were the container fails to run (aka created but then stopped)
def waitForContainerStable(container):
    print("Waiting for Container to stabilize...")

    while container.status == 'created':
        time.sleep(0.1)
        container.reload()

    print("Container Stabilized! --> ", container.status)
    

# TODO: make sure this only kills voyager workspace containers and nothing else
def killAllContainers():
    print("Killing all Containers...")
    containerList = client.containers.list()

    for container in containerList:
        container.kill()

    return True

def updateContainerStatus():
    containerList = client.containers.list()

    #get all 
    for container in containerList


def dictToContainerObj(attrs):
    
    attrsName = attrs['Name'].split('/')[1]
    attrsId = attrs['Id']
    attrsStatus = attrs['State']['Status']
    attrsImageName = attrs['Config']['Image']
    containerObj = WorkSpaceContainer(name=attrsName,
                                    id=attrsId,
                                    status=attrsStatus,
                                    imageName=attrsImageName,
                                    attrs=attrs
                                    )

    containerObj.save(force_insert=True)

    #TODO: figure out why the actual id is not being returned in the request
    # The sequential id (which is not actually stored in the db is being shown)
    print("THIS IS THE CONTAINER OBJ ___>", containerObj.id)
    return containerObj

# class ContainerObject():
#     def __init__(self, **kwargs):
#         self.name = kwargs['Name'].split('/')[1]
#         self.id = kwargs['Id']
#         self.status = kwargs['State']['Status']
#         self.imageName = kwargs['Config']['Image']
#         self.port = self.getContainerPort(kwargs)
        
#     def getContainerPort(self, attrs):
#         return attrs['NetworkSettings']['Ports'][defaultInternalPort + "/tcp"][0]['HostPort']

