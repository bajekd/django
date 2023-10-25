from django.contrib import admin

from .models import (Category, Product, ProductImage, ProductSpecification,
                     ProductSpecificationValue, ProductType)


@admin.register(Category)
class MPTTModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug"]


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = (ProductSpecificationInline,)


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductSpecificationValueInline, ProductImageInline)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "category", "product_type"]
