from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .form import Application_form
from django.http import JsonResponse
from .models import District, Branch


# def get_branches(request):
#     district_id = request.GET.get('district_id')
#     branches = Branch.objects.filter(dist=district_id)
#     branches_list = [{'id': branch.id, 'name': branch.name} for branch in branches]
#     print("selected branch", branches_list)
#     return JsonResponse({'branches': branches_list})


def get_branches(request, dist_id):
    branches = Branch.objects.filter(dist_id=dist_id).all()
    data = [{'id': branch.id, 'name': branch.name} for branch in branches]
    print("selected branch",data)
    return JsonResponse(data, safe=False)


def details(request):
    districts = District.objects.all()
    branches = Branch.objects.all()
    form = Application_form()
    if request.method == 'POST':
        form = Application_form(request.POST)
        if form.is_valid():
            dist_id = form.cleaned_data['district'].id
            form.update_branch_choices(dist_id)
            branch_id = form.cleaned_data['branch']
            return redirect('bank_app:success')

    return render(request, 'details.html', {'form': form, 'districts': districts, 'branches': branches})
    # return render(request, 'details.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def home(request):
    # Get the username from the session
    username = request.session.get('username', None)
    return render(request, 'index.html', {'username': username})


def register(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password == confirm_password:
            # Check if the username is not already taken
            if User.objects.filter(username=username).exists():
                error_message = "Username is already taken."
            else:
                # Create a new user
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                request.session['username'] = username
                return redirect('bank_app:index_login')
        else:
            error_message = "Passwords do not match."

    return render(request, 'register.html', {'error_message': error_message})


def index_login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username  # Set the username in the session
            return redirect('bank_app:details')  # Redirect to the home page after successful login
        else:
            error_message = "Invalid username or password"

    return render(request, 'index_login.html', {'error_message': error_message})


def logout_view(request):
    auth.logout(request)
    return redirect('bank_app:home')  # Redirect to your home page or another page after logout
