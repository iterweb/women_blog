from django import template
from django.db.models import Count, F
from django.core.cache import cache

from women.models import *


register = template.Library()


# @register.simple_tag(name='get_cats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)


@register.inclusion_tag('women/inc/_categories.html')
def show_categories(cat_selected=0):
    cats = cache.get('categories')
    if not cats:
        cats = Category.objects.annotate(cnt=Count('women', filter=F('women__is_published'))).filter(cnt__gt=0)
        cache.set('categories', cats, 60*15)


    return {'cats': cats, 'cat_selected': cat_selected}

