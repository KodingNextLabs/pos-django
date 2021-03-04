from django import forms

from pos.models import Order


class BuatOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'meja',
            'pelanggan',
        ]


class BayarOrderForm(forms.Form):
    dibayar = forms.IntegerField()