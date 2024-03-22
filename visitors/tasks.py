import logging

from django.db import OperationalError

from visitors.management.commands.run_scraper_counts import run_counts

log = logging.getLogger(__name__)


def run_stats() -> None:
    log.info("Recompute stats")
    try:
        # Too CPU demanding
        # run_statistics()
        run_counts()
    except (OperationalError, Exception) as error:
        log.exception(f"Error while computing stats: {error}")
