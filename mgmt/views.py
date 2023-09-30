from django.contrib.auth import logout as user_logout, login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from mgmt.custom_auth.models import User, UserEmailVerify, TOTPDevice, SignUpKey, UserActivateToken
from mgmt.form import LoginForm, ForgetForm, NewSetPasswordForm, SignUpForm, OTPForm


def sign_in(request):
    if request.user.is_authenticated:
        request.session.clear()
    auth_type = 'auth'
    invalid_code = False
    if request.method == 'POST':
        auth_type = request.POST.get("id", "auth")
        if auth_type == 'auth':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    request.session["user"] = user.id
                    auth_type = 'otp'
        elif auth_type == 'otp':
            form = OTPForm()
            auth_type = request.POST.get("otp_id", "auth_otp_email")
            if auth_type == "auth_otp_email":
                user = User.objects.get(id=int(request.session.get('user')))
                UserEmailVerify.objects.create_token(user=user)
            elif auth_type == 'auth_totp':
                user = User.objects.get(id=int(request.session.get('user')))
                if not TOTPDevice.objects.filter(user=user, is_active=True).exists():
                    invalid_code = 'TOTPデバイスが登録されていません。'

        elif auth_type == 'auth_otp_email':
            form = OTPForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=int(request.session.get('user')))
                is_exists = UserEmailVerify.objects.check_token(user_id=user.id, token=form.cleaned_data["token"])
                if is_exists:
                    user_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
            form = OTPForm()
            invalid_code = True
        elif auth_type == 'auth_totp':
            form = OTPForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=int(request.session.get('user')))
                is_exists = TOTPDevice.objects.check_totp(user=user, code=form.cleaned_data["token"])
                if is_exists:
                    user_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
            form = OTPForm()
            invalid_code = True
        else:
            form = LoginForm()
            request.session.clear()

    else:
        form = LoginForm()
        request.session.clear()
    context = {'type': auth_type, 'form': form, }
    if invalid_code:
        context['invalid_code'] = '認証コードが一致しません'
    return render(request, "sign_in.html", context)


@login_required
def sign_out(request):
    user_logout(request)
    context = {}
    return render(request, "sign_out.html", context)


def sign_up(request):
    key = ''
    key_error = ''
    error = ''
    form = SignUpForm()
    if request.method == 'POST':
        id = request.POST.get("id", "input_key")
        key = request.POST.get("key", "")
        form = SignUpForm(request.POST)
        if id == "input_key":
            if not SignUpKey.objects.check_key(key):
                key_error = '認証キーが異なります'

        else:
            if form.is_valid():
                try:
                    form.create_user(key)
                    return render(request, "sign_up_success.html", {})
                except ValueError as error:
                    print(error)
                    error = error
                except:
                    error = '何かしらのエラーが発生しました'
    context = {'form': form, 'key': key, 'key_error': key_error, 'error': error}
    print(context)

    return render(request, "sign_up.html", context)


class PasswordReset(PasswordResetView):
    subject_template_name = 'mail/password_reset/subject.txt'
    email_template_name = 'mail/password_reset/message.txt'
    template_name = 'forget.html'
    form_class = ForgetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'forget_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = NewSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'forget_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'forget_complete.html'


def activate_user(request, activate_token):
    message = 'ユーザーのアクティベーションが完了しました'
    try:
        UserActivateToken.objects.activate_user_by_token(activate_token)
    except ValueError as error:
        message = error
    except:
        message = 'エラーが発生しました。管理者に問い合わせてください'
    return render(request, "activate.html", {"message": message})


@login_required
def index(request):
    context = {}
    return render(request, "menu.html", context)

@login_required
def admin_sign_in(request):
    return redirect("sign_in")
