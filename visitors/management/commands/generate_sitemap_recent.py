# Generate sitemap for recently uploaded DNIs
import logging
import os
import math
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
import xml.etree.ElementTree as ET

from visitors.models import Visitor

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate sitemap for recently uploaded DNIs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1_000,
            help="Number of URLs per sitemap file (max 50000)",
        )
        parser.add_argument(
            "--output-dir", type=str, default="sitemaps", help="Directory to store sitemap files"
        )
        parser.add_argument(
            "--number-days",
            type=str,
            default="5",
            help="Include records created in the past number of days",
        )

    def handle(self, *args, **options):
        # Create output directory if it doesn't exist
        output_dir = os.path.join(settings.STATIC_ROOT, options["output_dir"])
        os.makedirs(output_dir, exist_ok=True)

        batch_size = options["batch_size"]
        self.stdout.write(f"Generating sitemaps with {batch_size} URLs per file...")

        # Count total DNIs
        visitors = Visitor.objects.filter(
            created_at__gte=datetime.now() - timedelta(days=int(options["number_days"]))
        )

        total_dnis = visitors.values("id_number").distinct().count()
        total_sitemaps = math.ceil(total_dnis / batch_size)

        self.stdout.write(
            f"Found {total_dnis} unique DNIs. Will generate {total_sitemaps} sitemap files."
        )

        # Generate individual sitemap files
        for i in range(total_sitemaps):
            self.generate_sitemap_file(output_dir, i, batch_size, visitors)
            self.stdout.write(f"Generated sitemap {i + 1}/{total_sitemaps}")

    def generate_sitemap_file(self, output_dir, index, batch_size, visitors):
        sitemap_name = self.find_next_sitemap_name(output_dir)
        offset = index * batch_size
        dnis = (
            visitors.values_list("id_number", flat=True)
            .distinct().order_by("id_number")[offset:offset + batch_size]
        )

        with open(os.path.join(output_dir, sitemap_name), "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

            for dni in dnis:
                f.write("  <url>\n")
                f.write(f"    <loc>https://manolo.rocks/visitas/{dni}/</loc>\n")
                f.write("    <changefreq>monthly</changefreq>\n")
                f.write("    <priority>0.5</priority>\n")
                f.write("  </url>\n")

            f.write("</urlset>")
        log.info(f"Sitemap file generated at {os.path.join(output_dir, f'sitemap_{index}.xml')}")
        self.add_to_sitemap_index(sitemap_name, output_dir)

    def find_next_sitemap_name(self, output_dir):
        existing_files = os.listdir(output_dir)
        existing_indices = [
            int(f.split("_")[1].split(".")[0])
            for f in existing_files
            if f.startswith("sitemap_")
            and f.endswith(".xml")
            and f.split("_")[1].split(".")[0].isdigit()
        ]
        next_index = max(existing_indices, default=-1) + 1
        return f"sitemap_{next_index}.xml"

    def add_to_sitemap_index(self, sitemap_name, output_dir):
        """Add a new sitemap entry to the sitemap index file"""
        index_file_path = os.path.join(output_dir, "sitemap.xml")
        today = datetime.now().strftime("%Y-%m-%d")

        # Check if sitemap index exists
        if os.path.exists(index_file_path):
            # Parse existing sitemap index
            try:
                tree = ET.parse(index_file_path)
                root = tree.getroot()
            except ET.ParseError:
                # If parsing fails, create a new index
                log.error(f"Failed to parse {index_file_path}")
                return
        else:
            log.error(f"Sitemap index file {index_file_path} does not exist")
            return

        # Check if this sitemap already exists in the index
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        existing_locs = [loc.text for loc in root.findall(".//ns:loc", namespace)]
        new_sitemap_url = f"https://manolo.rocks/static/sitemaps/{sitemap_name}"

        if new_sitemap_url not in existing_locs:
            # Create new sitemap element
            sitemap_elem = ET.SubElement(root, "sitemap")
            loc_elem = ET.SubElement(sitemap_elem, "loc")
            loc_elem.text = new_sitemap_url
            lastmod_elem = ET.SubElement(sitemap_elem, "lastmod")
            lastmod_elem.text = today

            # Write back to file
            tree.write(index_file_path, encoding="utf-8", xml_declaration=True)
            log.info(f"Added {sitemap_name} to sitemap index")
        else:
            log.info(f"Sitemap {sitemap_name} already exists in index")
