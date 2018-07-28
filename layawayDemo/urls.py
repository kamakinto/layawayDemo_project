"""layawayDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from .views import home_page #about_page, contact_page,  register_page,
from authentication.views import login_page #
from profiles.views import UserProfileView
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
#from carts.views import cart_home



urlpatterns = [
        path('', home_page, name='homepage'),
        path('login/', login_page, name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('profile/', include(("profiles.urls",  'profiles'), namespace='profiles')),
        path('request/', include(("item_requests.urls", 'request'), namespace='request')),
        path('dashboard/', include(("dashboard.urls",  'dashboard'), namespace='dashboard')),
        path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

