# product/management/commands/reindex_products.py

from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.documents import Document
from ...documents import ProductDocument

class Command(BaseCommand):
    help = 'Reindex all products into Elasticsearch'

    def handle(self, *args, **kwargs):
        ProductDocument().init()
        self.stdout.write(self.style.SUCCESS('Successfully reindexed products'))
