from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


def account_view(request):
    form = AuthenticationForm()
    return render(
        request,
        "account/account.html",
        {"form": form},
    )


@require_POST
@csrf_exempt
def ajax_login(request):
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        login(request, user)
        return JsonResponse({"success": True, "username": user.username})
    else:
        return JsonResponse({"success": False, "error": form.errors.as_json()})


@require_POST
@csrf_exempt
def ajax_logout(request):
    # Traitement de la déconnexion AJAX
    logout(request)
    return JsonResponse({"success": True})
