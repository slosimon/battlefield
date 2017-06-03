from unidecode import unidecode
from django.template.defaultfilters import slugify

def slug(value):
    return slugify(unidecode(value))

register.filter('slug', slug)
