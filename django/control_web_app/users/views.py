from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm

from main_menu.views import home_view

def register(request):
    """Register a new user"""
    if request.method != "POST":
        # Display blank registration form
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in ant then redirect to homepage.
            login(request, new_user)
            return redirect(home_view)

    # Display a blank or invalid form.
    context = {'form': form }
    return render(request, "registration/register.html", context)

# def logout(request):
#     logout(request)
#     print("Logged out")
#     return render(request, "registration/logged_out.html")

