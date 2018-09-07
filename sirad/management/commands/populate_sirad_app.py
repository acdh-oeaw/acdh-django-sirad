import os
from django.core.management.base import BaseCommand

from sirad.sirad import SiradReader


class Command(BaseCommand):
    help = "Populates your sirad-app with content from SIRAD-Archiv"

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='The name of your sirad-app application')

    def handle(self, *args, **kwargs):
        sirad_root = "legacy_data"
        app_name = kwargs['app_name']
        parsed = SiradReader(sirad_root)
        self.stdout.write(
            self.style.SUCCESS("{}".format('import started'))
        )
        import_data = parsed.populate_database(app_name)
        self.stdout.write(
            self.style.SUCCESS("{}".format('import ended'))
        )
