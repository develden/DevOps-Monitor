from django.urls import path
from .views import UserCreateView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Регистрация нового пользователя
    path('signup/', UserCreateView.as_view(), name='signup'),
    # Получение списка пользователей (только для аутентифицированных)
    path('users/', UserListView.as_view(), name='user-list'),
    # Эндпоинты JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 