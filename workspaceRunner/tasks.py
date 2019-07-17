from apscheduler.schedulers.background import BackgroundScheduler
from dockerController import updateContainerStatus
import docker

# TODO: investigate other ways to updateContainerStatus without continuously running a background job
# TODO: FIXME: Figure out why this runs twice...
def startBackgroundTasks():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(updateContainerStatus, trigger='interval', seconds=15)
    