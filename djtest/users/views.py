from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

@csrf_exempt
def field_function(request):
    """read fields from GET petition"""
    print(request.GET['numbers'])
    numbers = request.GET['numbers']
    numbers = [int(i) for i in numbers.split(',')]
    print('sorted: ' + str(sorted(numbers)))
    print(request.GET['letters'])

    data = {
        'status': 'ok',
        'numbers unsorted': request.GET['numbers'],
        'numbers sorted': str(sorted(numbers))
    }
    return HttpResponse(
        JsonResponse(data), content_type='application/json'
        )

@csrf_exempt
def age(request, name, age):
    """Return age validation"""
    if age > 18:
        message = "{} you are welcome".format(name)
    else:
        message = "{} you are rejected".format(name)

    return HttpResponse(message)

@csrf_exempt
def login(request):
    """read a json POST"""
    json_data = json.loads(request.body)
    try:
      data = json_data['user']
    except KeyError:
      return HttpResponseServerError("Malformed data!")

    return HttpResponse("I will create your user {}".format(json_data['user']))