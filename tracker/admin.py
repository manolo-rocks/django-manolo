from django.contrib import admin

from tracker.models import ScrapingPeriod


@admin.register(ScrapingPeriod)
class ScrapingPeriodAdmin(admin.ModelAdmin):
    list_display = [
        "institution",
        "period_display",
        "status",
        "records_scraped",
        "attempts",
        "last_attempt_at",
        "completed_at",
    ]
    list_filter = ["status", "start_date", "institution__name", "attempts"]
    search_fields = ["institution__name", "institution__abbreviation"]
    readonly_fields = ["created_at", "updated_at", "last_attempt_at", "completed_at"]
    date_hierarchy = "start_date"

    fieldsets = (
        ("Period Information", {"fields": ("institution", "start_date", "end_date", "status")}),
        (
            "Progress Tracking",
            {"fields": ("attempts", "max_attempts", "last_attempt_at", "completed_at")},
        ),
        ("Results", {"fields": ("records_scraped", "file_path", "file_size_bytes", "data_hash")}),
        ("Error Information", {"fields": ("error_message",), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    actions = ["retry_failed_periods", "mark_as_skipped"]

    def period_display(self, obj):
        return f"{obj.start_date.strftime('%Y-%m')}"

    period_display.short_description = "Period"
    period_display.admin_order_field = "start_date"

    def retry_failed_periods(self, request, queryset):
        retried = 0
        for period in queryset.filter(status="failed"):
            if period.retry():
                retried += 1

        self.message_user(request, f"Successfully queued {retried} periods for retry.")

    retry_failed_periods.short_description = "Retry selected failed periods"

    def mark_as_skipped(self, request, queryset):
        updated = queryset.update(status="skipped")
        self.message_user(request, f"Successfully marked {updated} periods as skipped.")

    mark_as_skipped.short_description = "Mark selected periods as skipped"
