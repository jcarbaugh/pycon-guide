import datetime
from django.core.management.base import BaseCommand, CommandError
from pyconguide.models import PyCon


class Command(BaseCommand):
    help = 'Create a new PyCon'

    def handle(self, *args, **options):

        today = datetime.date.today()
        year = int(input(f'What year is it? ({today.year}): ') or today.year)

        if PyCon.objects.filter(year=year).exists():
            raise CommandError(f'A PyCon already exists for {year}')

        loc = input(f'Where is PyCon {year}?: ')

        PyCon.objects.create(year=year, location=loc)
