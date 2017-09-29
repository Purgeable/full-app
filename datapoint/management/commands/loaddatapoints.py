from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from datapoint.models import Datapoint
from parsers.runner import Dataset


class Command(BaseCommand):
    help = 'Load datapoints to database using mini-kep parsers'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        saved = 0
        for data in Dataset.yield_dicts():
            datapoint = Datapoint(**data)
            try:
                datapoint.save()
                saved += 1
            except IntegrityError:
                self.stdout.write(self.style.WARNING('Failed to save datapoint\n%s' % data))

        self.stdout.write(self.style.SUCCESS('Successfully loaded %s datapoints' % saved))
