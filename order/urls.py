from django.urls import path

from .views import (MyClothOrdersAPIView,
                    MySentOrdersAPIView,
                    OrderAClothAPIView)

app_name = 'cloths'
urlpatterns = [
    path('orders/sent/', MySentOrdersAPIView.as_view()),
    path('orders/cloth/<int:id>/', MyClothOrdersAPIView.as_view()),
    path('order/<int:id>/',OrderAClothAPIView.as_view())
]