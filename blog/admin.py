from django.contrib import admin
from blog.models import Blog,Category


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'body_markdown', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}