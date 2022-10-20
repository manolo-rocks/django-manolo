from datetime import timedelta
import logging

from celery.task import periodic_task
from django.db import OperationalError

from visitors.management.commands.run_scraper_counts import run_counts
from visitors.management.commands.run_statistics import run_statistics

log = logging.getLogger(__name__)


@periodic_task(run_every=timedelta(minutes=60 * 24 * 7))
def run_stats() -> None:
    log.info("Recompute stats")
    try:
        # Too CPU demanding
        # run_statistics()
        run_counts()
    except (OperationalError, Exception) as error:
        log.exception(f"Error while computing stats: {error}")
