from django.conf.urls import url
from django.urls import path



from .views import  (
UserProfileView,
UserProfileEditView
)

urlpatterns = [
    path('', UserProfileView.as_view(), name='view'),
    path('edit/', UserProfileEditView.as_view(), name='edit'),

]

