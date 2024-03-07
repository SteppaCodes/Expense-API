from django.shortcuts import redirect
from django.views import View


class AutoRedirectView(View):
    def get(self, request):
        return redirect("api")
