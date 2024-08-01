from elasticsearch_dsl import Document, Text, Float, Keyword
from django.conf import settings
from products.models import ProductImage,Product

# Define the ProductDocument for Elasticsearch
class ProductDocument(Document):
    product_name = Text()
    product_description = Text()
    price = Float()
    category = Keyword()

    class Index:
        name = 'products'

# # Define the Product and ProductImage classes to hold search results
# class ProductResult:
#     def __init__(self, product_name, product_description, price=None, category=None, images=None):
#         self.product_name = product_name
#         self.product_description = product_description
#         self.price = price
#         self.category = category
#         self.images = images if images is not None else []

#     def __repr__(self):
#         return f"Product(name={self.product_name}, description={self.product_description}, price={self.price}, category={self.category}, images={self.images})"

# class ProductImageResult:
#     def __init__(self, image_url):
#         self.image_url = image_url

#     def __repr__(self):
#         return f"ProductImage(image_url={self.image_url})"

# # Perform the search query
# query = "your search query"
# response = ProductDocument.search().query("multi_match", query=query, fields=['product_name', 'product_description']).execute()

# # Convert each hit into a ProductResult instance and fetch related images
# products = []
# for hit in response:
#     # Fetch related images from the database
#     product_id = hit.meta.id  # Assuming the document ID matches the Product model's ID
#     product_instance = Product.objects.get(id=product_id)
#     product_images = ProductImage.objects.filter(product=product_instance)
    
#     images = [ProductImageResult(image_url=settings.MEDIA_URL + str(image.image)) for image in product_images]
    
#     product = ProductResult(
#         product_name=hit.product_name,
#         product_description=hit.product_description,
#         price=hit.price if 'price' in hit else None,
#         category=hit.category if 'category' in hit else None,
#         images=images
#     )
#     products.append(product)







# # products/documents.py

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from products.models import Product

# # Define the index
# products = Index('products')

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
