from django.conf.urls import url
from django.urls import path

from .views import (
        RequestCreationView,
        RequestDetailsView,
       RequestUpdateView,
       AddPaymentRequestView,
       ReviewPaymentView
)

urlpatterns = [
    path('create/', RequestCreationView.as_view(), name='create'),
    path('<slug>/', RequestDetailsView.as_view(), name='detail'),
    path('update/<slug>', RequestUpdateView.as_view(), name='update'),
    path('payment/<slug>', AddPaymentRequestView.as_view(), name='add'),
    path('payment/review/<slug>',ReviewPaymentView.as_view(), name='review')



]