import json

import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from visitors.models import KnownCandidate, Visitor


class Command(BaseCommand):
    help = 'Sync candidate data from Otorongo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--input_file',
            type=str,
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing candidates before syncing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing candidates...')
            KnownCandidate.objects.all().delete()

        input_file = options['input_file']

        with open(input_file, 'r') as file:
            candidates_data = json.loads(file.read())

        try:
            self.stdout.write(f'Found {len(candidates_data)} candidates to sync...')

            with transaction.atomic():
                created_count = 0
                updated_count = 0

                for candidate in candidates_data:
                    if not candidate['dni']:  # Skip if no DNI
                        continue

                    obj, created = KnownCandidate.objects.update_or_create(
                        dni=candidate['dni'],
                        defaults={
                            'full_name': candidate['full_name'],
                            'first_names': candidate['first_names'],
                            'last_names': candidate['last_names']
                        }
                    )

                    if created:
                        created_count += 1
                        print(f'Created new candidate: {obj.dni} - {obj.full_name}')
                    else:
                        updated_count += 1
                        print(f'Updated existing candidate: {obj.dni} - {obj.full_name}')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully synced candidates: {created_count} created, {updated_count} updated'
                )
            )

            self.stdout.write('Updating visitor candidate flags...')

            # Reset all flags
            Visitor.objects.update(is_candidate=False)

            # Get all candidate DNIs
            candidate_dnis = set(
                KnownCandidate.objects.values_list('dni', flat=True)
            )

            # Update visitors
            visitor_update_count = Visitor.objects.filter(
                id_document__in=candidate_dnis  # Change field name as needed
            ).update(is_candidate=True)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated {visitor_update_count} visitor records with candidate flags'
                )
            )

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data from Otorongo: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error syncing candidates: {e}')
            )
