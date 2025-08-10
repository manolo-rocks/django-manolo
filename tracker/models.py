from django.db import models
from django.utils import timezone

from visitors.models import Institution


class ScrapingPeriod(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("skipped", "Skipped"),
    ]

    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="scraping_periods"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Attempt tracking
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    last_attempt_at = models.DateTimeField(null=True, blank=True)

    # Completion tracking
    completed_at = models.DateTimeField(null=True, blank=True)
    records_scraped = models.PositiveIntegerField(default=0)
    file_path = models.CharField(max_length=500, blank=True)

    # Error handling
    error_message = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: store scraped data metadata
    data_hash = models.CharField(max_length=64, blank=True)  # For detecting changes
    file_size_bytes = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ["institution", "start_date", "end_date"]
        ordering = ["start_date", "institution__name"]
        indexes = [
            models.Index(fields=["status", "start_date"]),
            models.Index(fields=["institution", "status"]),
        ]

    def __str__(self):
        return f"{self.institution} - {self.start_date} to {self.end_date}"

    @property
    def period_name(self):
        return f"{self.start_date.strftime('%Y-%m')}"

    @property
    def can_retry(self):
        return self.status == "failed" and self.attempts < self.max_attempts

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    def mark_started(self):
        """Mark this period as started"""
        self.status = "in_progress"
        self.attempts += 1
        self.last_attempt_at = timezone.now()
        self.save()

    def mark_completed(self, records_scraped, file_path, file_size_bytes=None, data_hash=None):
        """Mark this period as completed"""
        self.status = "completed"
        self.completed_at = timezone.now()
        self.records_scraped = records_scraped
        self.file_path = file_path
        self.error_message = ""

        if file_size_bytes:
            self.file_size_bytes = file_size_bytes
        if data_hash:
            self.data_hash = data_hash

        self.save()

    def mark_failed(self, error_message):
        """Mark this period as failed"""
        self.status = "failed"
        self.error_message = error_message
        self.save()

    def retry(self):
        """Reset this period for retry"""
        if self.can_retry:
            self.status = "pending"
            self.error_message = ""
            self.save()

            return True
        return False
