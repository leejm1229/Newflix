from django.urls import path
from . import views

urlpatterns = [
    path('detailpage/<str:channel>/<str:url>', views.detail),
]