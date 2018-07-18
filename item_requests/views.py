from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import RequestForm, Request, UpdateRequestForm
from decimal import Decimal
import stripe
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

class RequestCreationView(FormView):
        template_name="request/create.html"
        request_form_class = RequestForm

        def get(self, request, *args, **kwargs):
                request_form_obj = self.request_form_class()
                return render(request, self.template_name, {
                        "request_form": request_form_obj
                })

        def post(self, request, *args, **kwargs):
                user = request.user
                new_request_form = RequestForm(request.POST)
                if new_request_form.is_valid():
                        new_request = new_request_form.save(commit=False)
                        new_request.user = user
                        new_request.save()
                        return redirect("dashboard:view")

                return render(request, "dashboard/view.html", {})

class AddPaymentRequestView(View):
        template_name="payment/create.html"

        def get(self, request, *args, **kwargs):
                user = request.user
                slug = self.kwargs.get('slug')
                #put a try block to get the right request object, if the user and the slug dont match, redirect the user to their dashboard
                try:
                        request_obj = Request.objects.get(user = user, slug=slug)
                except Request.DoesNotExist:
                        print("You are not the right user for this request")
                        return redirect("dashboard:view")
                else:
                        #request_obj = Request.objects.get(user = user)
                        # request_update_form = self.request_form_class(instance=request_obj)
                        return render(request, self.template_name, {
                                "request_obj": request_obj
                        })

        def post(self, request, *args, **kwargs):
                user = request.user
                slug = self.kwargs.get('slug')
                try:
                        request_obj = Request.objects.get(user = user, slug=slug)
                        amount_to_pay = request.POST.get("payment_amount")
                        request_obj.payment_amount = amount_to_pay
                        request_obj.save()
                except Request.DoesNotExist:
                        print("You are not the right user for this request")
                        return redirect("dashboard:view")
                else:
                        return redirect("request:review", slug=slug) #change to redirect to the review.html page once it has been plugged in

class ReviewPaymentView(View):
        template_name = "payment/review.html"

        def get(self, request, *args, **kwargs):
                user = request.user
                slug = self.kwargs.get('slug')
                try:
                        request_obj = Request.objects.get(user = user, slug=slug)
                        if request_obj.downpayment_paid:
                                stripe_amount = request_obj.payment_amount * 100
                                current_payment_amount = request_obj.payment_amount
                        else:
                                stripe_amount = request_obj.down_payment_amount * 100
                                current_payment_amount = request_obj.down_payment_amount

                except Request.DoesNotExist:
                        print("You are not the right user for this request")
                        return redirect("dashboard:view")
                else:
                        return render(request, self.template_name, {
                                "request_obj": request_obj,
                                "stripe_amount": stripe_amount,
                                "current_payment_amount": current_payment_amount
                        })

        def post(self, request, *args, **kwargs):
                user = request.user
                print(request.POST)
                slug = self.kwargs.get('slug')
                try:
                        request_obj = Request.objects.get(slug=slug, user = user)
                        payment_amount = request_obj.payment_amount
                        stripe.api_key = settings.STRIPE_SECRET_KEY
                        token = request.POST.get('stripeToken')
                        user_email = request.POST.get('stripeEmail')
                        stripe_payment_amount = int(request_obj.payment_amount)*100
                        customer = stripe.Customer.create(
                                email=user_email,
                                source = token
                        )
                        charge = stripe.Charge.create(
                                amount = stripe_payment_amount,
                                currency = "eur",
                                description = "New layaway payment",
                                customer = customer.id
                        )
                except stripe.error.CardError as e:
                        return False, e
                except Request.DoesNotExist:
                        print("You are not the right user for this request")
                        return redirect("dashboard:view")
                else:
                        #Payment was successful, handle any clean-up and processing
                        request_obj.payment_amount = 0.00
                        request_obj.remaining_amount -= payment_amount
                        request_obj.save()
                        #TODO:: Send a confirmation email to the user, and a notification email to the admins
                        return redirect("dashboard:view")



class RequestDetailsView(DetailView):
        model = Request
        template_name="request/detail.html"

        def get_object(self, *args, **kwargs):
                request = self.request
                user = request.user
                slug = self.kwargs.get('slug')
                try:
                        instance = Request.objects.get(slug=slug)
                except Request.DoesNotExist:
                        raise Http404("Not found..")
                except Request.MultipleObjectsReturned:
                        qs = Request.objects.filter(slug=slug)
                        instance = qs.first()
                except:
                        raise Http404("hmmmm")
                return instance


class RequestUpdateView(View):
        request_form_class = UpdateRequestForm
        template_name = 'request/request_update.html'

        def get(self, request, *args, **kwargs):
                user = request.user
                slug = self.kwargs.get('slug')
                request_obj = Request.objects.get(slug=slug)

                request_update_form = self.request_form_class(instance=request_obj)
                return render(request, self.template_name, {
                        'request_form': request_update_form
                })
        def post(self, request, *args, **kwargs):
                user = request.user
                slug=self.kwargs.get('slug')
                request_obj = Request.objects.get(slug=slug)

                request_form = self.request_form_class(request.POST, instance=request_obj)
                if request_form.is_valid():
                        if 'status' in request_form.changed_data:
                               # old_status = request_obj.status
                                # new_status = request.POST.get('status')
                                # send_mail(
                                #         'Testing for status changes',
                                #         'The status of your request has been updated to {0}. Please log-in to view your account'.format(new_status),
                                #         'haki.projects@gmail.com',
                                #         ['everettlrobinson@gmail.com'],
                                #         fail_silently=False,
                                # )


                                request_form.save()

                        #send an email to the Admins and User making the request of the updated status
                return redirect("dashboard:view")



