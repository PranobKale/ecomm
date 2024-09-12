from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name

class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    price = models.IntegerField()
    product_description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    mwk_flag = models.IntegerField(default=0,null=True,blank=True) #to categorise men-0, women-1 and kids-2 by flag.
    
 


    def save(self, *args,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name
    
    # def get_product_price_by_size(self,size):
    #     return self.price + SizeVariant.objects.get(size_name = size).price
    def get_product_price_by_size(self, size):
        try:
            size_variant = SizeVariant.objects.get(size_name=size)
            print(self.price + size_variant.price,"self.price + size_variant.price")
            return self.price + size_variant.price
        except SizeVariant.DoesNotExist:
            return self.price 
  
class ProductImage(BaseModel):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_image')
    image = models.ImageField(upload_to="product")

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

# Intermediary model to link Product, ColorVariant, and SizeVariant
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='variants')
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'color_variant', 'size_variant')