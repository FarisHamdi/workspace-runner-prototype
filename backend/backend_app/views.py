from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponseForbidden
from rest_framework import status, viewsets
from rest_framework.response import Response
from backend_app.models import Runner, Workspace
from backend.settings import RUNNER_KEY
from backend_app.serializers import RunnerSerializer, WorkspaceSerializer
import datetime, ast
import requests


class RunnerViewSet(viewsets.ModelViewSet):
    queryset = Runner.objects.all()
    serializer_class = RunnerSerializer

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

class RegisterRunner(APIView):

    def post(self, request, *args, **kwargs):
        runnerName = request.data['name']
        runnerUrl = request.data['url']
        apiKey = request.data['key']
        runnerId = request.data['id']
        runnerPort = request.data['port']

        print(runnerId)
        # check if key is valid
        if apiKey != RUNNER_KEY:
            return HttpResponseForbidden()

        runner = Runner.objects.create(id=runnerId,
                        name=runnerName,
                        url=runnerUrl,
                        port=runnerPort,
                        status='running')

        print("Runner Registered --> ", runner)

        return Response(status=status.HTTP_202_ACCEPTED)

class CoordinatorPing(APIView):
    def post(self, request, *args, **kwargs):

        runnerId = request.data['id']
        # containerList = request.data['containerList']
        containerList = request.POST['containerList']
       
        containerList = ast.literal_eval(containerList)
        updateWorkSpaces(containerList, runnerId)
        # check if runner is registered
        try: 
            runner = Runner.objects.get(id=runnerId)
            runner.lastContacted = datetime.datetime.now()
            runner.save()
            print('runner pinged! --> ', runner)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_202_ACCEPTED)

class CreateContainer(APIView):
    def post(self, request, *args, **kwargs):

        containerType = request.data['containerType']
        runnerId = request.data['runnerId']

        # get runner
        runner = Runner.objects.get(id=runnerId)  

        requestData = {
            'containerType': containerType
        }
        requestUrl = "http://" + runner.url + ':' + str(runner.port) + "/spinUpWorkspace/"

        req = requests.post(requestUrl, requestData)
        
        if req.status_code == 200:
            newWorkspace = createWorkspaceFromJson(req.json(), runnerId)
            serializer = WorkspaceSerializer(newWorkspace)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(req.status_code)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def updateWorkSpaces(containerList, runnerId):
    
    # get all workspaces from runner
    # inMemWorkSpaces = Workspace.objects.all().filter(runner_id==runnerId)
    # inMemWorkSpacesIds = [workspace.id for workspace in inMemWorkSpaces]
    containerListIds = [container['id'] for container in containerList]

    print('THE CONTAINER LIST IS  ', containerListIds)
    # for inMemWorkSpace in inMemWorkSpaces:
    #     if inMemWorkSpace.id in 

def createWorkspaceFromJson(json, runnerId):
    container = json['containerInstance']['attrs']
    port = container['NetworkSettings']['Ports']['8787' + "/tcp"][0]['HostPort']
    newWorkspace = Workspace.objects.create(runner_id = runnerId,
                                    id = container['Id'],
                                    environment= container['Config']['Image'],
                                    status= container['State']['Status'],
                                    port=port)
    print(newWorkspace)

    return newWorkspace

