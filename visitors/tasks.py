from datetime import timedelta
import logging

from celery.task import periodic_task
from django.db import OperationalError

from visitors.management.commands.run_statistics import run_statistics

log = logging.getLogger(__name__)


@periodic_task(run_every=timedelta(minutes=60 * 25))
def run_stats() -> None:
    log.info("Recompute stats")
    try:
        run_statistics()
    except (OperationalError, Exception) as error:
        log.exception(f"Error while computing stats: {error}")
