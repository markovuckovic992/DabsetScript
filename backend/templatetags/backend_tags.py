from django import template

register = template.Library()

@register.filter(name='strip')
def strip(string):
	print string.strip()
	return string.strip()