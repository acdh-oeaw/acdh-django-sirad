import os
from django.core.management.base import BaseCommand

from sirad.sirad import SiradReader


class Command(BaseCommand):
    help = "Creates a django app based upon SIRAD-Archiv"

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='The name of your new application')

    def handle(self, *args, **kwargs):
        sirad_root = "legacy_data"
        app_name = kwargs['app_name']
        parsed = SiradReader(sirad_root)
        files = parsed.generate_app_files(app_name=app_name)
        self.stdout.write(
            self.style.SUCCESS("{}".format('created'))
        )
