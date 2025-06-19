from django.http import JsonResponse


def email_confirmed_view(request):
    return JsonResponse({"detail": "Email successfully confirmed!"})