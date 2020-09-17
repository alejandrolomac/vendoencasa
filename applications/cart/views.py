from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from applications.product.models import Products, Color, Size, DiscountCode
from applications.wish.models import Wish, WishItem
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderForm

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
            order_item.quantity += prodquantity
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
            return redirect("product_app:single-product", slug=slug)
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
        return redirect("product_app:single-product", slug=slug)


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
def orderSummaryFinish(request):
    order = Order.objects.get(user=request.user, ordered=False, status='NoPagados')
    orCode = order.orderCode
    cantorder = order.items.count()
    price_total = Order.objects.get(user=request.user, ordered=False, status='NoPagados').get_total()
    title_product = Order.objects.get(user=request.user, ordered=False, status='NoPagados').stringNames()
    status = Order.objects.get(user=request.user, status='NoPagados')
    coupon = False
    coupons = ''
    shipping = 0
    discount_total = 0
    payMethod = ''
    stringsplit = ''

    if request.POST:
        if request.POST.get('location'):
            location = request.POST.get('location')
            locationsplit = location.split(', ')
            stringsplit = locationsplit[0]
            locationd = ''
            order.orderLocation = str(location)
            order.save()
            if str(locationsplit[0]) == 'Francisco Morazán':
                if cantorder == 1:
                    shipping = 80
                else:
                    cantordera = cantorder - 1
                    shipping = 80 + (20 * cantordera )
            else:
                shipping = 0
        else:
            if request.POST.get('newLocation'):
                location = request.POST.get('newLocation')
                locationd = request.POST.get('newLocationdir')
                order.orderLocation = str(location + ", " + locationd)
                order.save()
                if location == 'Francisco Morazán':
                    if cantorder == 1:
                        shipping = 80
                    else:
                        cantordera = cantorder - 1
                        shipping = 80 + (20 * cantordera )
                else:
                    shipping = 0
            else:
                messages.error(request, 'Tienes que elegir una dirección o introducir una nueva para continuar')
                return redirect("cart_app:orderpay")
                location = ''
                locationd = ''
        if request.POST.get('coupon'):
            coupons = DiscountCode.objects.get(code=request.POST.get('coupon'))
            if coupons:
                coupon = True
                if coupons.typediscount == 'Fijo':
                    discount_total = price_total - coupons.discount
                else:
                    discount_total = price_total * coupons.discount / 100
        if request.POST.get('customRadio'):
            payMethod = request.POST.get('customRadio')
            if  payMethod == 'Efectivo':
                order.payMethod = 'Efectivo'
            elif payMethod == 'Depósito Bancario':
                order.payMethod = 'Deposito'
            order.save()
        else:
            messages.error(request, 'Tienes que elegir un metodo de pago para continuar')
            return redirect("cart_app:orderpay")
            payMethod = ''
    context = {
        'object': order,
        'code': orCode,
        'status': status,
        'location': location,
        'locationd': locationd,
        'coupon': coupon,
        'coupons': coupons,
        'shipping': shipping,
        'discount_total': discount_total,
        'payMethod': payMethod,
        'stringsplit': stringsplit
    }
    return render(request, 'order_summary_finish.html', context)


@login_required(login_url='useradmin_app:entrar')
def orderSummaryEnd(request):
    order = Order.objects.get(user=request.user, ordered=False, status='NoPagados')
    order.paystaus = 'Procesando'
    order.status = 'Procesando'
    order.save()
    context = {
        'object': order
    }
    messages.error(request, 'Tu pedido está siendo procesado, dentro de poco tiempo serás contactado para más detalles')
    return redirect("/")


@login_required(login_url='useradmin_app:entrar')
def orderAdmin(request):
    orders = Order.objects.all().filter(status='Procesando')
    context = {
        'object': orders
    }
    return render(request, 'order_admin.html', context)



class OrderSummaryPay(LoginRequiredMixin, View):
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
            return render(self.request, 'order_summary_pay.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'No tienes ninguna lista de compras')
            return redirect("/")


class OrderSummaryFinish(LoginRequiredMixin, View):
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
            return render(self.request, 'order_summary_finish.html', context)
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
        order_item = OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False
        )[0]
        if order_item:
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Se actualizo el numero de productos")
            return redirect("cart_app:order")
    else:
        messages.info(request, "Se actualizo tu pedido")
        return redirect("cart_app:order")


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