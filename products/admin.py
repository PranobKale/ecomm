from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Coupon)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = SizeVariant

admin.site.register(Product, ProductAdmin)  # Register Product model with ProductAdmin

admin.site.register(ProductImage)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size_variant', 'color_variant']
    list_filter = ['size_variant', 'color_variant']
    search_fields = ['product__product_name', 'size_variant__size_name', 'color_variant__color_name']
