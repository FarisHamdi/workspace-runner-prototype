import docker
import utils

client = docker.from_env()
defaultInternalPort = '8787'

#TODO: organize container/template names by adding a template class, and associated functions 
def createContainer(containerType, username, projectName):

    randomPort = utils.randomPort()

    portSetting = {
       defaultInternalPort + "/tcp" : randomPort
    }

    if containerType == "jupyterLab":
        print("Starting JupyterLab Container...")
        container = client.containers.run("jupyterlab-workspace:latest", 
            auto_remove=False, detach = True, ports=portSetting)
    elif containerType == "rStudio":
        container = client.containers.run("rstudio-workspace:latest", 
            auto_remove=False, detach = True, ports=portSetting)

    containerInstance = ContainerObject(**container.__dict__['attrs'])


    return containerInstance

def getContainers():
    containerList = client.containers.list()
    fmtContainerList = []

    for container in containerList:
        fmtContainerList.append(ContainerObject(**container.__dict__['attrs']))

    return fmtContainerList

def killAllContainers():

    containerList = client.containers.list()

class ContainerObject():
    def __init__(self, **kwargs):
        self.name = kwargs['Name'].split('/')[1]
        self.id = kwargs['Id']
        self.status = kwargs['State']['Status']
        self.imageName = kwargs['Config']['Image']
        self.port = self.getContainerPort(kwargs)
        
    def getContainerPort(self, attrs):
        return [*attrs['NetworkSettings']['Ports'].keys()][0].split("/")[0]

