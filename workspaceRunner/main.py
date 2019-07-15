from sanic import Sanic
from sanic import response 
import dockerController
import json
import jsonpickle

app = Sanic()

@app.route("/listAllContainers/", methods=['GET'])
async def getRunningContainers(request):

    containerList = dockerController.getContainers()
    return response.json({"containerList": containerList})

@app.route("/spinUpWorkspace/",  methods=['POST'])
async def spinUpWorkspace(request):

    containerInstance = dockerController.createContainer(request.form['containerType'][0], 'test', 'e')
    return response.json({"containerInstance": containerInstance})

@app.route("/killAllContainers/", methods=['POST'])
async def killAllContainers(request):

    dockerController.killAllContainers()
    containerList = dockerController.getContainers()
    return response.json({"containerList": containerList})


app.static('/favicon.ico', './classic-blue.png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,auto_reload=True)

