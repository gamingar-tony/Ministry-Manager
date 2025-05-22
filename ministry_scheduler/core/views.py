from .forms import CustomUserCreationForm
from .models import ScheduleEntry, Schedule
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

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
    events = Schedule.objects.filter(user = request.user).order_by('date', 'time')
    return render(request, 'my_schedule.html', {'events': events})

@login_required
def schedule_view(request):
    all_events = Schedule.objects.select_related('user').order_by('date', 'time')
    return render(request, 'schedule.html', {'all_events': all_events})