from django.contrib import admin

from .models import Category, Product, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'description', 'is_active', 'price', 'created', 'updated']
    list_filter = ['is_active']
    list_editable = ['title', 'price', 'is_active', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['slug', 'title', 'languages', 'description', 'price', 'amount_of_days']
    list_editable = ['title', 'languages', 'price', 'amount_of_days', 'description']
    prepopulated_fields = {'slug': ('title',)}
    