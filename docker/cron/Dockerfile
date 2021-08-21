FROM manolo/manolo_app

COPY docker/cron/run_scraper.sh /code/cron_jobs/run_scraper.sh
RUN chmod a+x /code/cron_jobs/run_scraper.sh

COPY docker/cron/crontab /etc/crontab

# Run the command on container startup
CMD ["cron", "-f", "-L", "8"]
