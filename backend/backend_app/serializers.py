from rest_framework import serializers
from backend_app.models import Runner, Workspace

class RunnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runner
        fields = '__all__'

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

    