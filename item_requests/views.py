from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import RequestForm, Request

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

class RequestDetailsView(DetailView):
        model = Request
        template_name="request/detail.html"

        def get_object(self, *args, **kwargs):
                request = self.request
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



