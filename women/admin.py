from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_photo', 'title', 'time_create', 'time_update', 'is_published']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    list_filter = ['time_create', 'time_update', 'is_published']
    prepopulated_fields = {'slug': ['title']}
    fields = ['title', 'slug', 'category', 'content', 'photo', 'get_photo', 'is_published', 'time_create', 'time_update']
    readonly_fields = ['time_create', 'time_update', 'get_photo']

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="30">')
        else:
            return 'Нет фото'

    get_photo.short_description = 'Миниатюра'


admin.site.register(Women, WomenAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Category, CategoryAdmin)
