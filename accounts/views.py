from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import PasswordResetRequestForm, PasswordResetForm
import random
from django.utils import timezone

def custom_login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            # Authenticate by email or username
            user = authenticate(request, username_or_email=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to a success page.
            else:
                form.add_error(None, "Invalid login credentials")
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})
@login_required
def logout_view(request):
   logout(request)
   return redirect('/')




def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


# views.py





from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .forms import PasswordResetRequestForm, PasswordResetForm
import logging

logger = logging.getLogger(__name__)

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    link = request.build_absolute_uri(url)
                    subject = "Password Reset Requested"
                    message = render_to_string('accounts/password_reset_email.html', {
                        'user': user,
                        'link': link,
                    })
                    try:
                        send_mail(subject, message, 'awp.828.cr7@gmail.com', [user.email], fail_silently=False)
                    except Exception as e:
                        logger.error(f"Error sending email: {e}")
                return HttpResponse("An email has been sent to reset your password.")
    else:
        form = PasswordResetRequestForm()
    return render(request, "accounts/password_reset_request.html", {'form': form})

def password_reset_confirm(request, uidb64=None, token=None):
    if request.method == "POST":
        user = get_object_or_404(User, pk=force_str(urlsafe_base64_decode(uidb64)))
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = PasswordResetForm(user)
            else:
                return HttpResponse("Invalid token")
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            form = None
    return render(request, "accounts/password_reset_confirm.html", {'form': form})
