import stripe
from django.core.mail import send_mail

from config.settings import STRIPE_API_KEY, EMAIL_HOST_USER

stripe.api_key = STRIPE_API_KEY


# def create_stripe_price(product, price):
#     stripe_product = stripe.Product.create(
#         name=product
#     )
#     stripe_price = stripe.Price.create(
#         currency="rub",
#         unit_amount=price*100,
#         recurring={"interval": "month"},
#         product=stripe_product['id'],
#     )
#     return stripe_price['id']
#
#
# def create_stripe_session(stripe_price_id):
#     stripe_session = stripe.checkout.Session.create(
#         success_url="http://127.0.0.1:8000",
#         line_items=[{"price": stripe_price_id, "quantity": 1}],
#         mode="payment",
#     )
#     return stripe_session


def send_payment_link(url, email):
    send_mail(
        subject='Оплата курса',
        message=f'Ссылка для оплаты курса: {url}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email]

    )


def create_stripe_session(serializer):
    course_title = serializer.course.title
    stripe_product = stripe.Product.create(
        name=course_title
    )
    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=serializer.course.price * 100,
        recurring={"interval": "month"},
        product=stripe_product.id
    )
    stripe_session = stripe.checkout.Session.create(
        succes_ul="http://127.0.0.1:8000",
        line_items=[{"price": stripe_price.id, "quantity": 1}],
        mode="payment",
        customer_email=serializer.user.email,
    )
    send_payment_link(stripe_session.url, serializer.user.email)
    return stripe_session
