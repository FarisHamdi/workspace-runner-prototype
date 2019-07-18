import socket
import requests
import uuid
import settings, models, dockerController

def randomPort():
    """Get a single random port."""
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

#TODO: Move everything below somewhere else
def registerRunner():

    runnerId = uuid.uuid4()
    registrationData = {
        'name': settings.NAME,
        'url': settings.HOSTNAME,
        'port': settings.PORT,
        'key': settings.API_KEY,
        'id': str(runnerId),
    }

    req = requests.post('http://'+ settings.COORDINATOR_URL+'/registerRunner/', registrationData)

    if req.status_code == 202:
        registration = models.Registration(id = runnerId, coordinatorUrl=settings.COORDINATOR_URL)
        registration.save(force_insert=True)
    else:
        print(req.status_code)
        raise Exception("Registration Failed, coordinator returned a non 202 response")

def pingCoordinator():
    print("pinging cordinator...")

    # TODO: FIXME: figure out what to do with the case where more than one registration
    # instance exists
    reg = models.Registration.get()
    runnerId = reg.id

    containerList = dockerController.getRunningContainers()
    print('Container List, ping, ', containerList)

    pingData = {
        'id': str(runnerId),
        'containerList': str(containerList)
    }

    try:
        req = requests.post('http://'+ settings.COORDINATOR_URL+'/pingCoordinator/', pingData)
    except:
        raise Exception("Failed to connect to coordinator, unable to ping...")

    if req.status_code == 202:
        print("Yeah!", req)
    else: 
        raise Exception("Failed to connect to coordinator, coordinator returned a non 202 response: ", req)

def checkRegistration():

    print("checking registration...")
    if models.Registration.select().count() != 0:
        print("Registration exists in database")
        pingCoordinator()
    else:
        print("Runner is not Registered")
        print("Starting Registration process...")
        registerRunner()