from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, Textarea, TextInput
from django import forms


USER_ROLES = (
        ('admin', 'Administrator'),
        ('contributor', 'Contributor'),
        ('default_user', 'Default User')
)

class BillingAddress(models.Model):
        username = models.CharField(max_length=250, blank=True)
        address_line_1 = models.CharField(max_length=250, blank=True)
        address_line_2 = models.CharField(max_length=250, blank=True)
        city = models.CharField(max_length=250, blank=True)
        state = models.CharField(max_length=250, blank=True)
        postal_code = models.CharField(max_length=250, blank=True)

        def __str__(self):
                return str(self.username + ' - Billing Address')

class ShippingAddress(models.Model):
        username = models.CharField(max_length=250, blank=True)
        address_line_1 = models.CharField(max_length=250, blank=True)
        address_line_2 = models.CharField(max_length=250, blank=True)
        city = models.CharField(max_length=250, blank=True)
        state = models.CharField(max_length=250, blank=True)
        postal_code = models.CharField(max_length=250, blank=True)
        def __str__(self):
                return str(self.username + ' - Shipping Address')

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        email = models.EmailField(max_length=250, blank=True)
        first_name = models.CharField(max_length=250, blank=True)
        last_name = models.CharField(max_length=250, blank=True)
        role = models.CharField(max_length=100, choices=USER_ROLES, default='default_user')
        cell_number = models.CharField(max_length=250, blank=True)
        # photo =
        billing_address = models.OneToOneField(BillingAddress, null=True, on_delete=models.CASCADE)
        shipping_address = models.OneToOneField(ShippingAddress, null=True, on_delete=models.CASCADE)
        bio = models.TextField(max_length=500, blank=True)

        def __str__(self):
                return str(self.user.username)

class ProfileForm(ModelForm):
        """Form definition for Profile."""

        class Meta:
                model = Profile
                fields = ('email','first_name', 'last_name', 'cell_number', 'bio')
                widgets = {
                'email': TextInput(attrs={"class": "form-control"}),
                'first_name': TextInput(attrs={"class": "form-control"}),
                'last_name': TextInput(attrs={"class": "form-control"}),
                'cell_number': TextInput(attrs={"class": "form-control"}),
                'bio': Textarea(attrs={"cols":80, "rows":4, "class": "form-control"})
                }

class ShippingAddressForm(ModelForm):
        """Form definition for ShippingAddress."""

        class Meta:
                """Meta definition for ShippingAddressform."""

                model = ShippingAddress
                fields = ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code')
                widgets = {
                        'address_line_1': TextInput(attrs={"class": "form-control"}),
                        'address_line_2': TextInput(attrs={"class": "form-control"}),
                        'city': TextInput(attrs={"class": "form-control"}),
                        'state': TextInput(attrs={"class": "form-control"}),
                        'postal_code': TextInput(attrs={"class": "form-control"}),
                }

class BillingAddressForm(ModelForm):
        """Form definition for BillingAddress."""

        class Meta:
                """Meta definition for BillingAddressform."""

                model = BillingAddress
                fields = ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code')
                widgets = {
                        'address_line_1': TextInput(attrs={"class": "form-control"}),
                        'address_line_2': TextInput(attrs={"class": "form-control"}),
                        'city': TextInput(attrs={"class": "form-control"}),
                        'state': TextInput(attrs={"class": "form-control"}),
                        'postal_code': TextInput(attrs={"class": "form-control"}),
                }





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
        if created:
                new_shipping_address = ShippingAddress.objects.create(username=instance.username)
                new_billing_address = BillingAddress.objects.create(username=instance.username)
                Profile.objects.create(user=instance, billing_address=new_billing_address, shipping_address=new_shipping_address)





