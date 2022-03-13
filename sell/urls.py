from django.urls import path

from .views import (
    sellAPIview
    )

app_name='sell'
urlpatterns = [
    path('sell/<int:id>/',sellAPIview.as_view()),
]