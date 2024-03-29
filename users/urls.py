from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('create/', views.UserCreate.as_view(), name='user_create'),
    path('<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),

    path('payment/', views.PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/', views.PaymentCreateAPIView.as_view(), name='payment_create'),

    path('token/', TokenObtainPairView.as_view(), name='token_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
]
