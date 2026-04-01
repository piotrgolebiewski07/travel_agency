from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, pl, en):
    request = context.get('request')
    if request and request.LANGUAGE_CODE == 'pl':
        return pl
    return en

