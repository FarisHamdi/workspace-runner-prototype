from sanic import Sanic
from sanic.response import json as sjson
import dockerController
import json

app = Sanic()

@app.route("/")
async def test(request):

    containerList = dockerController.getContainers()
    return sjson({"containerList": json.dumps(containerList)})

app.static('/favicon.ico', './classic-blue.png')

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000,auto_reload=True)

