from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order


def checkout(request):
    return render(request, "checkout.html")


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    # LoginRequiredMixin : if required, redirects to the login page first
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, "order_summary.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # get_or_create : returns a tuple
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    # retrieve the cart items which is not ordered yet, from the explicit user
    order_queryset = Order.objects.filter(user=request.user, ordered=False)

    if order_queryset.exists():
        order = order_queryset[0]
        # if the item is in the cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('core:order-summary')

        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect('core:order-summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect('core:order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)

    # if an active cart exists
    if order_queryset.exists():
        order = order_queryset[0]
        # if the item is in the cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.quantity = 1
            order_item.save()
            messages.info(request, "This item was removed from your cart")
            return redirect('core:order-summary')

        else:
            messages.info(request, "This item is not in your cart")
            return redirect('core:order-summary')

    else:
        messages.info(request, "You do not have an active order")
        return redirect('core:order-summary')


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)

    # if an active cart exists
    if order_queryset.exists():
        order = order_queryset[0]
        # if the item is in the cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request, "This items quantity was updated")
            return redirect('core:order-summary')

        else:
            messages.info(request, "This item is not in your cart")
            return redirect('core:product', slug=slug)

    else:
        messages.info(request, "You do not have an active order")
        return redirect('core:product', slug=slug)
