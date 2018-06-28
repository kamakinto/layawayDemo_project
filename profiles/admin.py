from django.contrib import admin
from .models import Profile, BillingAddress, ShippingAddress
# Register your models here.
admin.site.register(Profile)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)