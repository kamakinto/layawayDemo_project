from django.conf.urls import url
from django.urls import path

from .views import (
        RequestCreationView,
        RequestDetailsView,
)

urlpatterns = [
    path('create/', RequestCreationView.as_view(), name='create'),
    path('<slug>/', RequestDetailsView.as_view(), name='detail'),

]