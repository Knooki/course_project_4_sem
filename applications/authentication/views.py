from distutils.command import config
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse

from django.contrib import auth

from .models import CustomUser

from django_countries import countries

from .forms import UserForm

COUNTRY_DICT = dict(countries)

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email не верный'}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Извините, этот email уже занят, используйте другой '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Никнейм должен содержать только буквенно-цифровые символы.'}, status=400)
        if str(username).isdecimal():
            return JsonResponse({'username_error': 'Никнейм не может состоять только из цифр.'})
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Извините, данный никнейм уже занят, выберите другой'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['country']
        
        password = request.POST['password']

        context = {
            'fieldValues': request.POST,
        }

        if not CustomUser.objects.filter(username=username).exists():
            if not CustomUser.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Пароль слишком короткий')
                    return render(request, 'authentication/register.html', context)

                user = CustomUser.objects.create_user(username=username, email=email, country=country, first_name=first_name, last_name=last_name, is_customer=True)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Активация аккаунта'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Здравствуйте, '+user.username + '! Пожалуйста перейдите по ссылке ниже для активации аккаунта\n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Аккаунт успешно создан')
                return render(request, 'authentication/login.html')

        return render(request, 'authentication/login.html')

    # def post(request):
    #     if request.method == 'POST':
    #         form = UserForm(request.POST)
    #         if form.is_valid():
    #             form.save()

    #     else:
    #         form = UserForm()
    #     return render(request, 'authentication/regitser.html', {'form': form})



class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'Пользователь уже активирован')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Аккаунт успешно активирован')
            return redirect('homepage')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Добро пожаловать, ' +
                                     user.username+', теперь вы вошли')
                    return redirect('homepage:homepage')
                messages.error(
                    request, 'Аккаунт еще не активирован. Пожалуйста проверьте свой email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Неверные данные, попробуйте снова')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Пожалуйста заполните все поля')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Вы вышли из аккаунта')
        return redirect('login')
