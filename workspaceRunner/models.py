from peewee import *
from settings import defaultInternalPort
from playhouse.hybrid import *
import datetime

db = SqliteDatabase('workspaceRunner.db')

class BaseModel(Model):
    class Meta:
        database = db

class WorkSpaceContainer(Model):
    name = CharField()
    id = CharField()
    status = CharField()
    imageName = CharField()
    attrs = TextField()
    lastUpdated = DateTimeField(default=datetime.datetime.now)

    @hybrid_property
    def port(self):
        return self.attrs['NetworkSettings']['Ports'][defaultInternalPort + "/tcp"][0]['HostPort']

    class Meta:
        database = db