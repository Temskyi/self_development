from django import template
register = template.Library()


@register.filter
def get_index_from_one(lst: list, value):
    return lst.index(value) + 1