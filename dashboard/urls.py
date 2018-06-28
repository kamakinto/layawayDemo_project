from django.conf.urls import url
from django.urls import path



from .views import  (
DashboardView
)

urlpatterns = [
    path('', DashboardView.as_view(), name='view'),
    #path('edit/', UserProfileEditView.as_view(), name='edit'),

]
