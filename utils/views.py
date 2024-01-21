from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse


def error_404(request, exception):
    message = (_("this endpoint is not found"))
    response = JsonResponse(data={"message":message, "status_code": 404})
    response.status_code = 404

    return response

def error_500(request):
    message = (_("An error occured, its on us"))
    response = JsonResponse(data={"message":message, "status_code": 500})
    response.status_code = 500
    
    return response