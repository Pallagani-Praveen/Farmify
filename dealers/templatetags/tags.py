from django import template

register = template.Library()

@register.filter(name='sub')
def subtract(value,arg):
    return value-arg

@register.filter(name='mul')
def multiply(value,arg):
    return value*arg

@register.filter(name='div')
def divide(value,arg):
    return value/arg

@register.filter(name='abs')
def divide(value):
    return abs(value)

@register.filter(name='strip_user')
def strip_user(email):
    return email[:email.index('@')]

@register.filter(name='cap_the_first')
def cap_the_first(strg):
    return strg.capitalize()

@register.filter(name='count')
def count(arr):
    return len(arr)


