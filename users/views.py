from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from learning.models import Course
from users.permissions import IsOwner, IsModer
from users.models import Payment, User, Subscription
from users.serializers import PaymentSerializer, UserSerializer, SubscriptionSerializer


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
    filterset_fields = ('course', 'lesson', 'method')
    search_fields = ['course', 'lesson', 'method']
    ordering_fields = ['pay_day']


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """
        Create a new subscription instance and assign it to the current owner
        """
        course_id = self.kwargs.get('pk')
        course = Course.objects.get(pk=course_id)
        subscription = serializer.save(owner=self.request.user, course=course, is_active=True)
        subscription.save()


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

    def destroy(self, request, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        user_id = self.request.user.pk

        subscription = Subscription.objects.get(course_id=course_id, owner_id=user_id)

        if self.request.user != subscription.user:
            raise serializers.ValidationError('Нельзя удалить чужую подписку!')
        else:
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
