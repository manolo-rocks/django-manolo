# your_app/management/commands/generate_sitemaps.py
import os
import math
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

from visitors.models import Visitor


class Command(BaseCommand):
    help = 'Generate static XML sitemap files for DNI search pages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size', type=int, default=5000,
            help='Number of URLs per sitemap file (max 50000)'
        )
        parser.add_argument(
            '--output-dir', type=str, default='sitemaps',
            help='Directory to store sitemap files'
        )

    def handle(self, *args, **options):
        # Create output directory if it doesn't exist
        output_dir = os.path.join(settings.STATIC_ROOT, options['output_dir'])
        os.makedirs(output_dir, exist_ok=True)

        batch_size = options['batch_size']
        self.stdout.write(f"Generating sitemaps with {batch_size} URLs per file...")

        # Count total DNIs
        total_dnis = Visitor.objects.values('id_number').distinct().count()
        total_sitemaps = math.ceil(total_dnis / batch_size)

        self.stdout.write(
            f"Found {total_dnis} unique DNIs. Will generate {total_sitemaps} sitemap files."
        )

        # Generate sitemap index file
        self.generate_sitemap_index(output_dir, total_sitemaps)

        # Generate individual sitemap files
        for i in range(total_sitemaps):
            self.generate_sitemap_file(output_dir, i, batch_size)
            self.stdout.write(f"Generated sitemap {i + 1}/{total_sitemaps}")

    def generate_sitemap_index(self, output_dir, total_sitemaps):
        today = datetime.now().strftime('%Y-%m-%d')

        with open(os.path.join(output_dir, 'sitemap.xml'), 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

            for i in range(total_sitemaps):
                f.write('  <sitemap>\n')
                f.write(f'    <loc>https://manolo.rocks/static/sitemaps/sitemap_{i}.xml</loc>\n')
                f.write(f'    <lastmod>{today}</lastmod>\n')
                f.write('  </sitemap>\n')

            f.write('</sitemapindex>')

    def generate_sitemap_file(self, output_dir, index, batch_size):
        offset = index * batch_size
        dnis = Visitor.objects.values_list('id_number', flat=True).distinct().order_by('id_number')[
        offset:offset + batch_size]

        with open(os.path.join(output_dir, f'sitemap_{index}.xml'), 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

            for dni in dnis:
                f.write('  <url>\n')
                f.write(f'    <loc>https://manolo.rocks/visitas/{dni}/</loc>\n')
                f.write('    <changefreq>monthly</changefreq>\n')
                f.write('    <priority>0.5</priority>\n')
                f.write('  </url>\n')

            f.write('</urlset>')