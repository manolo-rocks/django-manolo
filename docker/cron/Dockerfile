FROM manolo/manolo_app

COPY docker/cron/run_scraper_congreso.sh /code/cron_jobs/run_scraper_congreso.sh
RUN chmod a+x /etc/cron.daily/run_scraper_congreso.sh

# Run the command on container startup
CMD ["cron", "-f", "-L", "8"]
