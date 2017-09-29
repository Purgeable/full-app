from django.core.management.base import BaseCommand, CommandError
from datapoint.models import Datapoint
from parsers.runner import Dataset


class Command(BaseCommand):
    help = 'Load datapoints to database using mini-kep parsers'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        objs = Datapoint.objects.bulk_create(map(lambda data: Datapoint(**data), Dataset.yield_dicts()))
        self.stdout.write(self.style.SUCCESS('Successfully loaded %s datapoints' % len(objs)))
