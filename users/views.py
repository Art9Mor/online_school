from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import Course
from users.models import Payment, User, Subscription
from users.serializers import PaymentSerializer, UserSerializer, SubscriptionSerializer
# from users.services import create_stripe_price, create_stripe_session
from users.services import create_stripe_session


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdate(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('paid_course', 'paid_lesson', 'method')
    search_fields = ['paid_course', 'paid_lesson', 'method']
    ordering_fields = ['pay_day']


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    # def perform_create(self, serializer):
    #     course_id = self.kwargs.get('pk')
    #     course = Course.objects.get(pk=course_id)
    #     user = self.request.user
    #     price_id = create_stripe_price(
    #         product=serializer.course.title,
    #         price=serializer.course.price
    #     )
    #
    #     if Payment.objects.filter(paid_course=course, owner=user).exists():
    #         return ValidationError('This course is already paid')
    #     else:
    #         serializer.save(
    #             paid_course=course,
    #             owner=user,
    #             paid_sum=course.price * 100,
    #             method=self.request.method,
    #             payment_session=create_stripe_session(price_id)
    #         )

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if not course:
            raise serializers.ValidationError('Course is required.')
        payment = serializer.save()
        payment.user = self.request.user
        if payment.method == 'Transfer':
            payment.payment_session = create_stripe_session(payment).id
        payment.save()


class SubscriptionView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user

        course_id = request.data.get('course_id')
        course = course_id.objects.get_object_or_404()

        subscription = Subscription.objects.filter(owner=user, course=course, is_active=True)

        if user != subscription.owner:
            raise serializers.ValidationError('Нельзя удалить чужую подписку!')
        else:
            if subscription.exists():
                subscription.delete()
                message = 'подписка удалена'

            else:
                Subscription.objects.create(owner=user, course=course, is_active=True)
                message = 'подписка добавлена'

            return Response({"message": message}, {'user': user})

