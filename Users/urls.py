from django.urls import path

from .views import (
    LoginAPIView ,
    RegistrationAPIView,
    UserListAPIView, 
    UserPrivateAPIView, 
    UserPublicAPIView,
    UserReactivate
    )

app_name = 'Users'
urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('profile/public/<int:id>/', UserPublicAPIView.as_view()),
    path('profile/private/<int:id>/',UserPrivateAPIView.as_view()),
    path('users/', UserListAPIView.as_view()),
    path('reactivate/<int:id>/',UserReactivate.as_view()),
]
