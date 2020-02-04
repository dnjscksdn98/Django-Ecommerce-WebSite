from django import template
from core.models import Order

# register template tag
register = template.Library()

# register custom filter
@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        queryset = Order.objects.filter(user=user, ordered=False)

        if queryset.exists():
            return queryset[0].items.count()

    return 0
