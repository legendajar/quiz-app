from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
from django.contrib.auth.decorators import login_required
from quiz.models import QuizSubmission


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1 == password2:
            
            # if username is not same
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            
            # if email is not same
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken')
                return redirect('register')
            
            # if username and email are valid
            else:
                # create user
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                
                # log in the user and redirect to profile
                user_login = auth.authenticate(username=username, password=password1)
                auth.login(request, user_login)

                # create profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('profile', user_model.username)

        else:
            messages.error(request, 'Password does not match')
            return redirect('register')
                                 
    return render(request, 'register.html')

@login_required(login_url='login')
# Profile View
def profile(request, username):

    # request user
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)


    # profile user
    user_object2 = User.objects.get(username=username)
    user_profile2 = Profile.objects.get(user=user_object2)

    submissions = QuizSubmission.objects.filter(user=user_object2)


    context={
        'user_object': user_object,
        'user_profile': user_profile,
        'user_object2': user_object2,
        'user_profile2': user_profile2,
        'submissions': submissions,
    }
    return render(request, 'profile.html', context)


# Edit Profile View
@login_required(login_url='login')
def editProfile(request):

    # request user
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":

        #Image
        if request.FILES.get('profileimg') is not None:
            user_profile.profileimg = request.FILES.get('profileimg')
            user_profile.save()

        # Email
        if request.POST.get('email') is not None:
            u = User.objects.filter(email=request.POST.get('email')).first()

            if u == None:
                user_object.email = request.POST.get('email')
                user_object.save()

            else:
                if u != user_object:
                    messages.error(request, 'Email is already taken')
                    return redirect('editProfile')
        
        # Username
        if request.POST.get('username') is not None:
            u = User.objects.filter(username=request.POST.get('username')).first()

            if u == None:
                user_object.username = request.POST.get('username')
                user_object.save()
            else:
                if u!= user_object:
                    messages.error(request, 'Username is already taken')
                    return redirect('editProfile')
        
        # First Name
        user_object.first_name = request.POST.get('first_name')

        # Last Name
        user_object.last_name = request.POST.get('last_name')

        user_object.save()



        #Location
        user_profile.location = request.POST.get('location')

        # Gender
        user_profile.gender = request.POST.get('gender')

        # Bio
        user_profile.bio = request.POST.get('bio')

        user_profile.save()


        return redirect('profile', user_object.username)

    context={"user_profile":user_profile}
    return render(request, 'profile-edit.html',context)

# Delete Profile View
@login_required(login_url='login')
def delProfile(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        user_profile.delete()
        user_object.delete()
        return redirect('logout')
    

    context = {
        "user_profile": user_profile,

    }
    
    return render(request, 'confirm.html', context)

# Login View
def login(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile', username)
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
        
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')