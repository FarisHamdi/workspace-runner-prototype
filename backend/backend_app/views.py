from django.shortcuts import render
from rest_framework.views import APIView
from backend_app.models import Runner
from backend.settings import RUNNER_KEY
from django.http import HttpResponseForbidden
from rest_framework import status
from rest_framework.response import Response

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

        return Response(status=status.HTTP_202_ACCEPTED)

