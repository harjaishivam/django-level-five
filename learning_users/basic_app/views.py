from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# imports for LOGIN
from django.contrib.auth import authenticate, login, logout
# from django.core.urlresolvers import reverse
from django.urls import  reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special_page(request):
    return HttpResponse('you are logged in, nice!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            #Here, we are hashing the password fieled of the User, and saving that in the database.
            user.set_password(user.password)
            user.save()

            #We use commit = Flase, so that the profile form does not try to override the user.
            profile = profile_form.save(commit = False)
            profile.user = user # This is the main line that ensures only one instance of each user is present.
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic'] # This simply ensures that we get the profile pic that django has stored inside request

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)


    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/register.html', {'user_form':user_form,
                                                           'profile_form':profile_form,
                                                           'registered':registered})

# never call your view login, as you are importing login above, and then it will be overriden.
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # User is automatically authenticated by this one single line
        user = authenticate(username=username, password=password)

        if user:
            #check paranthesis afet is_active
            if user.is_active:
                login(request, user)
                # if they have logged in successfully, reverse them and redirect them back to home page.
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE!')
        else:
            print('Someone tried to log in and failed.')
            print('username: ' + username + ' and password: ' + password)
            return HttpResponse('Invalid login details supplied.')
    else:

        return render(request, 'basic_app/login.html', {})
