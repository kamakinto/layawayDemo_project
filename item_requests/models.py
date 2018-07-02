from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, Textarea, TextInput, ChoiceField, NumberInput, CheckboxInput, Select, SelectDateWidget
from django import forms
from django.urls import reverse
from layawayDemo.utils import unique_order_id_generator, unique_slug_generator
from django.db.models.signals import pre_save


REQUEST_STATUS = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
)
class Request(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        reference_ID = models.CharField(max_length=250, blank=True, default='xxx')
        url = models.CharField(max_length=250, blank=True, null=True)
        status = models.CharField(max_length=50, choices=REQUEST_STATUS, default='pending')
        slug = models.SlugField(blank=True, unique=True)
        title = models.CharField(max_length = 120, default='layaway request')
        submission_date = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        purchase_date = models.DateTimeField(blank=True, null=True)
        notes = models.CharField(max_length=250, blank=True, null=True)
        price =models.DecimalField(decimal_places=2, max_digits=20, default=00.00)
        remaining_amount = models.DecimalField(decimal_places=2, max_digits=20, default=00.00)
        payment_amount = models.DecimalField(decimal_places=2, max_digits=20, default=00.00)
        downpayment_paid = models.BooleanField(default=False)


        def __str__(self):
                return str( self.status)

        def get_absolute_url(self):
                return reverse("request:detail", kwargs={"slug": self.slug})


class RequestForm(ModelForm):
        """Form definition for Request."""

        class Meta:
                """Meta definition for Requestform."""

                model = Request
                fields = ('url', 'notes')
                widgets = {
                        'url': TextInput(attrs={"class": "form-control"}),
                        'notes': Textarea(attrs={"cols":80, "rows":4, "class": "form-control"})
                }

class UpdateRequestForm(ModelForm):
        """Form definition for UpdateRequest."""

        class Meta:
                model = Request
                fields = ('status', 'title', 'notes', 'purchase_date',  'price', 'remaining_amount', 'payment_amount', 'downpayment_paid')
                widgets = {
                        'status': Select(attrs={"class": "form-control"}),
                        'title': TextInput(attrs={"class": "form-control"}),
                        'price': TextInput(attrs={"class": "form-control"}),
                        'purchase_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"), attrs={"class": "form-control"}),
                        'remaining_amount': NumberInput( attrs={"class": "form-control"}),
                        'payment_amount': NumberInput(attrs={"class": "form-control"}),
                        'downpayment_paid': CheckboxInput( attrs={"class": "form-control"}),
                        'notes': Textarea(attrs={"cols":80, "rows":4, "class": "form-control"})

                }




@receiver(pre_save, sender=Request)
def pre_save_request_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
                instance.slug = unique_slug_generator(instance)

        #get current user
        #Create reference ID
        #create Slug
        #save current user object to the user field

        pass









