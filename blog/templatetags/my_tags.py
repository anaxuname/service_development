from django import template

register = template.Library()


@register.filter()
@register.simple_tag()
def my_media(val):
    if not val:
        return ''
    return "/media/" + str(val)
