from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import ProfileForm, Profile, ShippingAddress, ShippingAddressForm, BillingAddress, BillingAddressForm

class UserProfileView(View):
        profile_form_class = ProfileForm
        template_name = "profile/user_view.html"
        greeting = "hello and welcome"
        # user = get currently logged in user


        def get(self, request, *args, **kwargs):
                user = request.user
                profile = Profile.objects.get(pk=user.id)
                profile_object = self.profile_form_class(instance=profile)
                #form = self.profile_form_class()
                print(profile)
                return render(request, self.template_name, {
                        "greeting": self.greeting,
                         "profile": profile})



class UserProfileEditView(View):
        profile_form_class = ProfileForm
        shipping_address_form_class = ShippingAddressForm
        billing_address_form_class = BillingAddressForm
        template_name = "profile/user_edit.html"
        greeting = "hello and welcome"
        # user = get currently logged in user


        def get(self, request, *args, **kwargs):
                user = request.user
                profile = Profile.objects.get(pk=user.id)
                shipping_address = ShippingAddress.objects.get(username=user.username)
                billing_address = BillingAddress.objects.get(username=user.username)

                profile_form = self.profile_form_class(instance=profile)
                shipping_address_form = self.shipping_address_form_class(prefix='ship', instance=shipping_address)
                billing_address_form = self.billing_address_form_class(prefix='bills', instance=billing_address)
                return render(request, self.template_name, {
                        "greeting": self.greeting,
                        "profile_form": profile_form,
                        "shipping_form": shipping_address_form,
                        "billing_form": billing_address_form
                        }
                        )
        def post(self, request, *args, **kwargs):
                #get the currect instance of each of the objects being edited
                user = request.user
                profile = Profile.objects.get(pk=user.id)
                shipping_address = ShippingAddress.objects.get(username=user.username)
                billing_address = BillingAddress.objects.get(username=user.username)
                #Get the form data being changed
                profile_form = self.profile_form_class(request.POST, instance=profile)
                shipping_form = self.shipping_address_form_class(request.POST, instance=shipping_address, prefix='ship')
                billing_form = self.billing_address_form_class(request.POST, instance= billing_address, prefix='bills' )
                #validate form data and update the object
                if profile_form.is_valid() and shipping_form.is_valid() and billing_form.is_valid():
                        shipping_form.save()
                        billing_form.save()
                        profile_form.save()
                        pass

                return render(request, self.template_name, {
                        "greeting": self.greeting,
                        "profile_form": profile_form,
                        "shipping_form": shipping_form,
                        "billing_form": billing_form
                        }
                        )

