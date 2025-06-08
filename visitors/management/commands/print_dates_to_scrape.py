from django.db import connection
from django.db.models import Min, Max

from django.core.management import BaseCommand

from visitors.models import Visitor


class Command(BaseCommand):
    help = "Print dates that need scraping"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        analyze_all_institutions()


def get_all_institutions():
    """Get list of all institutions in the database"""
    return Visitor.objects.values_list('institution', flat=True).distinct()


def find_missing_dates_by_institution(institution, start_date=None, end_date=None):
    """
    Find dates that have no visitor records for a specific institution.

    Args:
        institution (str): Name of the institution to check
        start_date (datetime.date, optional): Start date for the search
        end_date (datetime.date, optional): End date for the search

    Returns:
        tuple: (list of missing dates, date_range dict with min and max dates)
    """
    # If no dates provided, get them from the database for this institution
    if not start_date or not end_date:
        date_range = Visitor.objects.filter(institution=institution).aggregate(
            min_date=Min('date'),
            max_date=Max('date')
        )
        start_date = date_range['min_date']
        end_date = date_range['max_date']

        if not start_date or not end_date:
            return [], {'min_date': None, 'max_date': None}

    # Use raw SQL for better performance
    query = """
    WITH RECURSIVE date_series(date) AS (
        SELECT date_trunc('day', %s::timestamp)::date
        UNION ALL
        SELECT (date + '1 day'::interval)::date
        FROM date_series
        WHERE date < %s::date
    ),
    dates_with_records AS (
        SELECT DISTINCT date::date
        FROM visitors_visitor
        WHERE institution = %s
        AND date BETWEEN %s::date AND %s::date
    )
    SELECT date_series.date
    FROM date_series
    LEFT JOIN dates_with_records ON date_series.date = dates_with_records.date
    WHERE dates_with_records.date IS NULL
    ORDER BY date_series.date;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date, institution, start_date, end_date])
        missing_dates = [row[0] for row in cursor.fetchall()]

    return missing_dates, {'min_date': start_date, 'max_date': end_date}


def print_institution_report(institution, missing_dates, date_range):
    """
    Print a formatted report of missing dates for a specific institution
    """
    if not date_range['min_date']:
        print(f"\n{institution}:")
        print("No records found for this institution")
        return

    total_missing = len(missing_dates)
    total_days = (date_range['max_date'] - date_range['min_date']).days + 1
    coverage_percent = ((total_days - total_missing) / total_days) * 100

    print(f"\n{institution}:")
    print("=" * 50)
    print(f"Date range: {date_range['min_date']} to {date_range['max_date']}")
    print(f"Total days in range: {total_days}")
    print(f"Days with no records: {total_missing}")
    print(f"Coverage: {coverage_percent:.1f}%")

    if missing_dates:
        print("\nMissing dates by month:")
        print("-" * 50)

        current_month = None
        for date in missing_dates:
            month = date.strftime("%B %Y")
            if month != current_month:
                current_month = month
                print(f"\n{month}:")
            print(f"  - {date.strftime('%d/%m/%Y')} ({date.strftime('%A')})")


def analyze_all_institutions(start_date=None, end_date=None):
    """
    Analyze missing dates for all institutions
    """
    institutions = get_all_institutions()

    if not institutions:
        print("No institutions found in the database!")
        return

    print("\nAnalyzing visitor records by institution...")
    print(
        "Date range:", f"{start_date} to {end_date}" if start_date and end_date else "Full dataset"
    )

    for institution in sorted(institutions):
        if institution:  # Skip null values
            missing_dates, date_range = find_missing_dates_by_institution(
                institution, start_date, end_date
            )
            print_institution_report(institution, missing_dates, date_range)
