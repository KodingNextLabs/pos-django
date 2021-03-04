from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError

from pos.forms import BuatOrderForm, BayarOrderForm
from pos.models import Menu, Order, Item


def home(request):
    return render(request, 'pos/home.html')


def daftar_menu(request, order_id):
    menu_list = Menu.objects.all()
    order = get_object_or_404(Order, pk=order_id)

    page = request.GET.get('page', 1)
    
    paginator = Paginator(menu_list, 10)
    
    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)
    
    return render(request, 
                  'pos/daftar_menu.html', 
                  {'menus': menus,
                   'order': order})
    

def buat_order(request):
    if request.method == 'POST':
        form = BuatOrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.total = 0
            obj.dibayar = 0
            obj.kembali = 0
            obj.save()
            return redirect('pos:daftar-menu', order_id=obj.pk)

    else:
        form = BuatOrderForm()
    return render(request, 'pos/buat_order.html', {'form': form})


def order_aktif(request):
    order_list = Order.objects.filter(selesai=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(order_list, 10)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request,
                  'pos/order_aktif.html',
                  {'orders': orders})


def tambah_item(request, order_id, menu_id):
    order = get_object_or_404(Order, id=order_id)
    menu = get_object_or_404(Menu, id=menu_id)
    item, created = Item.objects.get_or_create(
        menu=menu,
        order=order
    )

    item.qty = item.qty + 1
    item.harga = menu.price
    item.subtotal = item.harga * item.qty
    item.save()

    items = Item.objects.filter(order=order).aggregate(total=Sum('subtotal'))
    order.total = items['total']
    order.save()

    return redirect('pos:daftar-menu', order_id=order.id)


def batal_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return redirect('pos:order-aktif')


def bayar_order(request, id):
    order = get_object_or_404(Order, id=id, selesai=False)

    if request.method == 'POST':
        form = BayarOrderForm(data=request.POST)

        if form.is_valid():
            dibayar = form.cleaned_data['dibayar']

            if dibayar < order.total:
                raise ValidationError('Uang Anda kurang!')

            order.kembali = dibayar - order.total
            order.dibayar = dibayar
            order.selesai = True
            order.save()

            return render(
                request,
                'pos/print_order.html',
                {'order': order}
            )

    else:
        form = BayarOrderForm()

    return render(request,
                  'pos/bayar_order.html',
                  {'order': order, 'form': form})


def print_order(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'pos/print_order.html', {'order': order})



def buat_item(request):
    pass


def ubah_status_item(request):
    pass


def cetak_struk(request):
    pass

