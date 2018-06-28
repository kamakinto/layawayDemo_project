from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from item_requests.models import Request
from profiles.models import Profile

class DashboardView(View):
        template_name = "dashboard/view.html"
        greeting = "hello and welcome to your dashboard"
        user_request_obj = None
        user_request_list = None
        admin_role = False
        # user = get currently logged in user
        def get(self, request, *args, **kwargs):
                if request.user.is_authenticated:
                        user = request.user
                        try:
                                self.admin_role = self.isAdmin(user)
                                self.user_request_obj = Request.objects.get(user=user)
                                if self.admin_role:
                                        self.user_request_list = Request.objects.all()
                                        pending_requests = self.user_request_list.filter(status="pending")
                                        under_review_requests = self.user_request_list.filter(status="under_review")
                                        approved_requests = self.user_request_list.filter(status="approved")
                                        rejected_requests = self.user_request_list.filter(status="rejected")
                        except Request.DoesNotExist:
                                print("This user has no item requests")
                        except Request.MultipleObjectsReturned:
                                print("multiple requests")
                                qs = Request.objects.get(user=user)
                                self.user_request_obj = qs.first()
                else:
                        print("User shouldnt be here...not logged in")

                return render(request, self.template_name, {
                        "greeting": self.greeting,
                        "request_obj": self.user_request_obj,
                        "purchases": None,
                        "is_admin": self.admin_role,
                        "pending_requests": pending_requests,
                        "under_review_requests": under_review_requests,
                        "approved_requests": approved_requests,
                        "rejected_requests": rejected_requests})
        def isAdmin(self, user):
                current_user_profile = Profile.objects.get(user=user)
                is_admin = True if current_user_profile.role == "admin" else  False
                return is_admin



