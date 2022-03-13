from django.urls import path

from .views import (
    AllClothsAPIView,
    AllAvailableClothsAPIView,
    ClothAPIView,
    CertainUserCloth,
    AuthenticatedUserCloth,
    )

app_name='cloths'
urlpatterns = [
    path('cloth/<int:id>/',ClothAPIView.as_view()),
    path('cloths/',AllAvailableClothsAPIView.as_view()),
    path('allcloths/',AllClothsAPIView.as_view()),
    path('user/cloths/',CertainUserCloth.as_view()),
    path('mycloths/',AuthenticatedUserCloth.as_view())
]