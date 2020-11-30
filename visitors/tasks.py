from datetime import timedelta
import logging

from celery.canvas import chain
from celery.task import periodic_task
from django.db import OperationalError

from manolo.celery import app
from scrapers.manolo_scraper.spiders.ambiente import AmbienteSpider
from scrapers.manolo_scraper.spiders.congreso import CongresoSpider
from visitors.management.commands.run_statistics import run_statistics

log = logging.getLogger(__name__)


@periodic_task(run_every=timedelta(minutes=60 * 25))
def run_stats() -> None:
    log.info("Recompute stats")
    try:
        run_statistics()
    except (OperationalError, Exception) as error:
        log.exception(f"Error while computing stats: {error}")


@periodic_task(run_every=timedelta(minutes=60 * 24))
def schedule_spiders() -> None:
    # for spider in spiders
    # schedule crawl with delay (create a celery chain)
    spiders = [
        AmbienteSpider,
        CongresoSpider,
    ]

    tasks = []

    for spider in spiders:
        task = schedule_crawl.si(spider.name)
        tasks.append(task)

    task_chain = chain(*tasks)
    task_chain.apply_async()


@app.task
def schedule_crawl(spider_name: str) -> None:
    print(spider_name)
