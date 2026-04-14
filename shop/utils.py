from django.core.mail import send_mail


def send_order_email(order):
    send_mail(
        subject=f'Новый заказ #{order.id}',
        message=f'Заказ от {order.first_name} {order.last_name}',
        from_email='your@email.com',
        recipient_list=[order.email],
    )
