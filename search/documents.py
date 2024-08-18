from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from products.models import Product

# Define the document
@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    class Index:
        # Name of the Elasticsearch index
        name = 'products'

    class Django:
        model = Product  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'product_name',
            'slug',
            'price',
            'product_description',
        ]
