from django import template
from ..models import Company, Category, SubCategory, Products
from applications.cart.models import Order

register = template.Library()

@register.inclusion_tag('list-cats-header.html')
def show_cats_header():
	return {'catsheader': Category.objects.all()}
	

@register.filter
def cart_item_count(user):
	if user.is_authenticated:
		qs = Order.objects.all().filter(user=user, ordered=False)
		if qs.exists():
			return qs[0].items.count()
	
	return 0