import base64
from io import BytesIO

import pyotp
import qrcode
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mgmt.custom_auth.form import TwoAuthForm
from mgmt.custom_auth.models import TOTPDevice


@login_required
def index(request):
    context = {}
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        if id == 'two_auth':
            return redirect('custom_auth:list_two_auth')
    return render(request, "user/profile.html", context)


@login_required
def add_two_auth(request):
    error = None
    initial_check = TOTPDevice.objects.check_max_totp_device(user=request.user)
    secret = TOTPDevice.objects.generate_secret()
    form = TwoAuthForm()
    buffer = BytesIO()
    qrcode.make(secret.get('url')).save(buffer, format="PNG")
    qr = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        if id == 'submit' and initial_check:
            form = TwoAuthForm(request.POST)
            otp_secret = request.POST.get("secret")
            if form.is_valid():
                code = form.cleaned_data['code']
                verify_code = pyotp.TOTP(otp_secret).verify(code)
                if verify_code:
                    TOTPDevice.objects.create_secret(
                        user=request.user,
                        title=form.cleaned_data['title'],
                        otp_secret=otp_secret
                    )
                    return redirect("custom_auth:list_two_auth")
                else:
                    error = "コードが一致しません"
            else:
                error = "request error"
        else:
            error = "request error"

    context = {
        'initial_check': initial_check,
        'secret': secret.get('secret'),
        'url': secret.get('url'),
        'qr': qr,
        'form': form,
        'error': error
    }

    return render(request, "user/two_auth/add.html", context)


@login_required
def list_two_auth(request):
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        device_id = int(request.POST.get('device_id', 0))
        if id == 'delete':
            TOTPDevice.objects.remove(id=device_id, user=request.user)
    context = {'devices': TOTPDevice.objects.list(user=request.user)}
    return render(request, "user/two_auth/list.html", context)
