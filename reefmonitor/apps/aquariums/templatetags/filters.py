from django import template

import dateutil.parser

register = template.Library()

@register.filter(name='hash')
def hash(map, key):
    print(map)
    return map[key]

@register.filter(name='value')
def value(map, key):
    return map[key]["value"]

@register.filter(name='timestamp')
def timestamp(map, key):
    return dateutil.parser.parse(map[key]["timestamp"])

@register.simple_tag
def define(val=None):
    return val