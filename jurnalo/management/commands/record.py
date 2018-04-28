from django.core.management.base import BaseCommand
from jurnalo.models import Record
import dateutil.parser
from datetime import datetime

class Command(BaseCommand):
    help='Adds a new record'

    def add_arguments(self, parser):
        parser.add_argument('--raw')


    def handle(self, *args, **options):
        records = Record.objects.order_by('id').all()[:1]
        previous_record = None
        if len(records) > 0:
            previous_record = records[0]
        raw_record = options['raw'].split(';')
        record = Record()
        record.text = raw_record[1]
        record.creator = Entity.objects.get(urn=raw_record[2])
        record.on_behalf_of = None
        record.previous_record = previous_record
        record.created_at = datetime.now()
        record.passed_at = dateutil.parser.parse(raw_record[0])
