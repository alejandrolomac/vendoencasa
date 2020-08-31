from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from applications.product.models import Products, Color, Size
from applications.wish.models import Wish, WishItem
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='useradmin_app:entrar')
def add_to_cart(request, slug):
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
        prodquantity = request.POST.get('product_quantity')
    else: 
        colorid = ''
        prodquantity = 1
        sizeid = ''
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        color=colorid,
        size=sizeid,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False,
        status='NoPagados')
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug, color=order_item.color, size=order_item.size).exists():
            order_item.quantity = prodquantity
            order_item.save()
            messages.info(request, "Se actualizo el numero de productos")
            return redirect("cart_app:order")
        else:
            messages.success(request, "Se agrego el producto al carrito")
            order.items.add(order_item)
            order_item.color = colorid
            order_item.size = sizeid
            order_item.quantity = prodquantity
            order_item.save()
            return redirect("cart_app:order")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date, status='NoPagados')
        order.orderCode = str(order.id) + '-' + str(request.user.id) + '-' + str(order.ordered_date.strftime('%Y%m%d'))
        order.items.add(order_item)
        order.save()
        order_item.color = colorid
        order_item.size = sizeid
        order_item.quantity = prodquantity
        order_item.save()
        messages.success(request, "Se agrego el producto al carrito")
        return redirect("cart_app:order")


@login_required(login_url='useradmin_app:entrar')
def add_to_cart_from_wish(request, slug):
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
        prodquantity = request.POST.get('product_quantity')
    else: 
        colorid = ''
        prodquantity = 1
        sizeid = ''
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        color=colorid,
        size=sizeid,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_ws = Wish.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        orderw = order_ws[0]
        if order.items.filter(item__slug=item.slug, color=order_item.color, size=order_item.size).exists():
            order_item.quantity = prodquantity
            order_item.save()
            if orderw.items.filter(item__slug=item.slug).exists():
                orderw.items.filter(item__slug=item.slug).delete()
            messages.info(request, "Se actualizo el numero de productos")
            return redirect("cart_app:order")
        else:
            messages.success(request, "Se agrego el producto al carrito")
            order.items.add(order_item)
            order_item.color = colorid
            order_item.size = sizeid
            order_item.quantity = prodquantity
            order_item.save()
            if orderw.items.filter(item__slug=item.slug).exists():
                orderw.items.filter(item__slug=item.slug).delete()
            return redirect("cart_app:order")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.orderCode = str(order.id) + '-' + str(request.user.id) + '-' + str(order.ordered_date.strftime('%Y%m%d'))
        order.items.add(order_item)
        order.save()
        order_item.color = colorid
        order_item.size = sizeid
        order_item.quantity = prodquantity
        order_item.save()
        if orderw.items.filter(item__slug=item.slug).exists():
                orderw.items.filter(item__slug=item.slug).delete()
        messages.success(request, "Se agrego el producto al carrito")
        return redirect("cart_app:order")



@login_required(login_url='useradmin_app:entrar')
def remove_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        order_item = OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False
        )[0]
        if order.items.filter(item__slug=item.slug).exists():
            #order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Se elimino el producto del carrito")
        else:
            messages.error(request, "Este producto no existe en tu carrito")
            return redirect("product_app:single-product", slug=slug)
            
    else:
        messages.info(request, "El carrito esta vacio")
        return redirect("product_app:single-product", slug=slug)
    return redirect("product_app:single-product", slug=slug)

@login_required(login_url='useradmin_app:entrar')
def remove_from_cart_c(request, slug, color):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        order_item = OrderItem.objects.filter(
            item=item,
            color=color,
            user=request.user,
            ordered=False
        )[0]
        if order.items.filter(item__slug=item.slug, color=order_item.color).exists():
            #order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Se elimino el producto del carrito")
        else:
            messages.error(request, "Este producto no existe en tu carrito")
            return redirect("product_app:single-product", slug=slug)
            
    else:
        messages.info(request, "El carrito esta vacio")
        return redirect("product_app:single-product", slug=slug)
    return redirect("product_app:single-product", slug=slug)



@login_required(login_url='useradmin_app:entrar')
def remove_from_cart_s(request, slug, size):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        order_item = OrderItem.objects.filter(
            item=item,
            size=size,
            user=request.user,
            ordered=False
        )[0]
        if order.items.filter(item__slug=item.slug, size=order_item.size).exists():
            #order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Se elimino el producto del carrito")
        else:
            messages.error(request, "Este producto no existe en tu carrito")
            return redirect("product_app:single-product", slug=slug)
            
    else:
        messages.info(request, "El carrito esta vacio")
        return redirect("product_app:single-product", slug=slug)
    return redirect("product_app:single-product", slug=slug)


@login_required(login_url='useradmin_app:entrar')
def remove_from_cart_sc(request, slug, color, size):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        order_item = OrderItem.objects.filter(
            item=item,
            color=color,
            size=size,
            user=request.user,
            ordered=False
        )[0]
        if order.items.filter(item__slug=item.slug, color=order_item.color, size=order_item.size).exists():
            #order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Se elimino el producto del carrito")
        else:
            messages.error(request, "Este producto no existe en tu carrito")
            return redirect("product_app:single-product", slug=slug)
            
    else:
        messages.info(request, "El carrito esta vacio")
        return redirect("product_app:single-product", slug=slug)
    return redirect("product_app:single-product", slug=slug)




class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False, status='NoPagados')
            orCode = order.orderCode
            price_total = Order.objects.get(user=self.request.user, ordered=False, status='NoPagados').get_total()
            title_product = Order.objects.get(user=self.request.user, ordered=False, status='NoPagados').stringNames()
            status = Order.objects.get(user=self.request.user, status='NoPagados')
            context = {
                'object': order,
                'code': orCode,
                'status': status
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'No tienes ninguna lista de compras')
            return redirect("/")


@login_required(login_url='useradmin_app:entrar')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                #order.items.remove(order_item)
                order_item.delete()
            return redirect("cart_app:order")
        else:
            return redirect("product_app:single-product", slug=slug)
    else:
        return redirect("product_app:single-product", slug=slug)


@login_required(login_url='useradmin_app:entrar')
def clean_cart(request):
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        order.delete()

    return redirect("product_app:index")