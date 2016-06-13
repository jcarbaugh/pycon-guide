from django.core.management.base import BaseCommand
from pyconguide import schedule


class Command(BaseCommand):
    help = 'Scrape PyCon schedule and import'

    def handle(self, *args, **options):
        schedule.scrape_pycon()
