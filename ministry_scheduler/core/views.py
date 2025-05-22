from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ScheduleEntry

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    from django.contrib.auth.forms import AuthenticationForm

    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def home_view(request):
    upcoming = ScheduleEntry.objects.filter(user = request.user, date__gte = timezone.now().date()).order_by('date')[:5]
    return render(request, 'home.html', {
        'user': request.user,
        'upcoming': upcoming,
    })

@login_required
def my_schedule(request):
    # Placeholder - you'll betch user-specific events later
    events = []
    return render(request, 'my_schedule.html', {'events': events})