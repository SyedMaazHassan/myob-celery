from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
# from pymyob.api import MYOB
# from pymyob.auth import AuthorizationCodeAuthenticator
import requests
from accounts.task import send_email_task_with_celery
from django.core.mail import send_mail


MYOB_CLIENT_ID = '&&&**&^*&^*^*^*'
MYOB_CLIENT_SECRET = '&&&**&^*&^*^*^*'
MYOB_REDIRECT_URI = 'http://127.0.0.1:8000/accounts/myob/callback'

# Set up the authenticator
# authenticator = AuthorizationCodeAuthenticator(
#     client_id=MYOB_CLIENT_ID,
#     client_secret=MYOB_CLIENT_SECRET,
#     redirect_uri=MYOB_REDIRECT_URI,
#     scope='CompanyFile',
# )

def my_new_task():
    print("Running my_new_task...")

def myob_login(request):
    authorization_url = 'https://secure.myob.com/oauth2/account/authorize'

    params = {
        'client_id': MYOB_CLIENT_ID,
        'redirect_uri': MYOB_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'CompanyFile',
    }

    redirect_url = f"{authorization_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return redirect(redirect_url)



def myob_callback(request):
    token_url = 'https://secure.myob.com/oauth2/v1/authorize'
    token_endpoint = 'https://secure.myob.com/oauth2/v1/token'

    code = request.GET.get('code')

    data = {
        'client_id': MYOB_CLIENT_ID,
        'client_secret': MYOB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': MYOB_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }


    response = requests.post(token_endpoint, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print(response.json())
        # Store the access token for further API requests
        # Implement your own logic here

        return HttpResponse('Success!')
    else:
        # Handle error case
        return HttpResponse('Failure!')




def send_email_task_without_celery():
    send_mail(
        'Task without celery Worked!',
        'This is proof the task worked!',
        'hafizmaazhassan33@gmail.com',
        ['syedmaazhussain33@gmail.com'],
        fail_silently=False
    )
    return None



def home_view(request):
    # return redirect('myob_login')
    send_email_task_with_celery.delay()
    return HttpResponse('Hello, World!')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
