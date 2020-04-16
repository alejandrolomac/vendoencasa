from django import template
from ..models import Company, Category, SubCategory, Products

register = template.Library()

@register.inclusion_tag('list-cats-header.html')
def show_cats_header():
	return {'catsheader': Category.objects.all()}
	

