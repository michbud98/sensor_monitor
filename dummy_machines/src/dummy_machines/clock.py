from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import dummy_machines.requester as requester

import logging

# Set logging to DEBUG which prints additional information
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

def scheduled_job(args: dict = dict()):
    """
    Job that is run on schedule.

    Args:
        args (dict, optional): [description]. Defaults to dict().
    """
    logging.debug(f'Running scheduled job. Args: {args}')
    requester.make_request(**args)


def main():
    sched = BlockingScheduler()

    # sched.add_job(scheduled_job, args=[{"device_type": requester.DeviceType.BLINDS, "id": 1}], trigger='interval', minutes=45)
    sched.add_job(scheduled_job, args=[{"device_type": requester.DeviceType.BLINDS, "id": 2}], trigger='interval', seconds=5)
    # sched.add_job(scheduled_job, trigger='interval', seconds=5)

    logging.info("Jobs scheduled.")
    sched.start()
