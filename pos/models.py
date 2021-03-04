from django.db import models

"""
Migrations for 'pos':
  pos/migrations/0001_initial.py
    - Create model Menu
    - Create model Order
    - Create model Item
"""


class Menu(models.Model):
    nama = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=10000)
    image = models.URLField()
    
    def __str__(self):
        return self.nama
    

class Order(models.Model):
    meja = models.CharField(max_length=100)
    pelanggan = models.CharField(max_length=100)
    total = models.PositiveIntegerField(default=0)
    dibayar = models.PositiveIntegerField(default=0)
    kembali = models.PositiveIntegerField(default=0)
    selesai = models.BooleanField(default=False)

    def __str__(self):
        return self.meja

    
class Item(models.Model):
    order = models.ForeignKey(Order,
                              related_name='order_item', 
                              on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, 
                             related_name='menu_item', 
                             on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    harga = models.PositiveIntegerField(default=0)
    subtotal = models.PositiveIntegerField(default=0)
    catatan = models.CharField(max_length=200, blank=True, null=True)
    dikirim = models.BooleanField(default=False)
    
    def __str__(self):
        return self.menu.nama
    

    
    