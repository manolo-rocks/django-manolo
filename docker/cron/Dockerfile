FROM manolo/manolo_app

COPY docker/cron/crontab /etc/crontab

# Run the command on container startup
CMD ["cron", "-f", "-L", "8"]
