# Assuming this code is in your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def filename_mask(image_file):
    file = image_file.split('\\')
    filesplit = image_file.split('/')
    filename = filesplit[2]
    return filename


