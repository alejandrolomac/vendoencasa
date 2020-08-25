from django.shortcuts import render, get_object_or_404, redirect
from .models import Wish, WishItem
from applications.product.models import Products, Color, Size
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='useradmin_app:entrar')
def add_to_whis(request, slug):
    item = get_object_or_404(Products, slug=slug)
    if request.POST:
        if request.POST.get('colorlist'):
            colorid = request.POST.get('colorlist')
        else:
            colorid = ''
        if request.POST.get('sizelist'):
            sizeid = request.POST.get('sizelist')
        else:
            sizeid = ''
    else: 
        colorid = ''
        sizeid = ''
    order_item, created = WishItem.objects.get_or_create(
        item=item,
        color=colorid,
        size=sizeid,
        user=request.user,
        ordered=False
    )
    order_qs = Wish.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug, color=order_item.color, size=order_item.size).exists():
            order_item.save()
            messages.info(request, "Se agrego el producto a tu lista de deseos")
            return redirect("product_app:single-product", slug=slug)
        else:
            messages.success(request, "Se agrego el producto a tu lista de deseos")
            order.items.add(order_item)
            order_item.color = colorid
            order_item.size = sizeid
            order_item.save()
            return redirect("product_app:single-product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Wish.objects.create(user=request.user, ordered_date=ordered_date)
        order.orderCode = str(order.id) + '-' + str(request.user.id) + '-' + str(order.ordered_date.strftime('%Y%m%d'))
        order.items.add(order_item)
        order.save()
        order_item.color = colorid
        order_item.size = sizeid
        order_item.save()
        messages.success(request, "Se agrego el producto a tu lista de deseos")
        return redirect("product_app:single-product", slug=slug)


@login_required(login_url='useradmin_app:entrar')
def remove_from_whis(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Wish.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        order_item = WishItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False
        )[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.filter(item__slug=item.slug).delete()
            messages.info(request, "Se elimino el producto de la lista de deseos")
        else:
            messages.error(request, "Este producto no existe en tu lista de deseos")
            return redirect("product_app:single-product", slug=slug)
            
    else:
        messages.info(request, "Tu lista de deseos esta vacia")
        return redirect("product_app:single-product", slug=slug)
    return redirect("product_app:single-product", slug=slug)


class WishSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Wish.objects.get(user=self.request.user, ordered=False)
            orCode = order.orderCode
            context = {
                'object': order,
                'code': orCode,
            }
            return render(self.request, 'wish.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'No tienes ninguna lista de deseos')
            return redirect("/")