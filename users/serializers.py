from rest_framework import serializers

from users.models import Payment, User, Subscription
from users.services import create_stripe_price, create_stripe_session


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payment_link = serializers.SerializerMethodField(read_only=True)

    def get_payment_link(self, incoming):
        price_id = create_stripe_price(
            product=incoming.course.title,
            price=incoming.course.price * 100
        )
        payment_link = create_stripe_session(price_id)
        return payment_link

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
