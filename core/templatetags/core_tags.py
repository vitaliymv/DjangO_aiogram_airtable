import dateutil.parser
from django import template

register = template.Library()


@register.filter()
def convert_date(row):
    d = dateutil.parser.parse(row)
    return d.strftime('%d-%m-%Y')
