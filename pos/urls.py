from django.urls import path
from pos import views

app_name = 'pos'

urlpatterns = [
    path('', views.home, name='home'),
    path('new-order/', views.buat_order, name='buat-order'),
    path('daftar-menu/<int:order_id>/', views.daftar_menu, name='daftar-menu'),
    path('tambah-item/<int:order_id>/<int:menu_id>/', views.tambah_item, name='tambah-item'),
    path('order-aktif/', views.order_aktif, name='order-aktif'),
    path('print-order/<int:id>/', views.print_order, name='print-order'),
    path('batal-order/<int:id>/', views.batal_order, name='batal-order'),
    path('bayar-order/<int:id>/', views.bayar_order, name='bayar-order'),
]
