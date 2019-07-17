from peewee import *
from settings import defaultInternalPort
from playhouse.hybrid import *
import datetime, ast

db = SqliteDatabase('workspaceRunner.db')

class BaseModel(Model):
    class Meta:
        database = db

class WorkSpaceContainer(Model):
    name = CharField()
    id = CharField(primary_key=True)
    username = CharField()
    project_id = UUIDField()
    status = CharField()
    imageName = CharField()
    attrs = TextField()
    lastUpdated = DateTimeField(default=datetime.datetime.now)

    @hybrid_property
    def port(self):

        parsed_attrs = ast.literal_eval(self.attrs)
        return parsed_attrs['NetworkSettings']['Ports'][defaultInternalPort + "/tcp"][0]['HostPort']

    class Meta:
        database = db

    def dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'username': self.username,
            'project_id': str(self.project_id),
            'status': self.status,
            'imageName': self.imageName,
            # 'attrs': self.attrs,
            'lastUpdated': str(self.lastUpdated),
            'port': self.port
        }