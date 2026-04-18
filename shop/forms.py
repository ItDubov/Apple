from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order


# 🛒 ЗАКАЗ
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Почта'),
            'phone': _('Телефон'),
            'address': _('Адрес'),
        }


# 📩 КОНТАКТЫ
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_('Имя')
    )

    email = forms.EmailField(
        label=_('Почта')
    )

    message = forms.CharField(
        widget=forms.Textarea,
        label=_('Сообщение')
    )