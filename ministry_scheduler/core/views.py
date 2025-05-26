from .forms import CustomUserCreationForm, UserUpdateForm
from .models import ScheduleEntry, Schedule
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    # Placeholder - you'll fetch user-specific events later
    events = Schedule.objects.filter(user = request.user).order_by('date', 'time')
    return render(request, 'my_schedule.html', {'events': events})

@login_required
def schedule_view(request):
    all_events = Schedule.objects.select_related('user').order_by('date', 'time')
    return render(request, 'schedule.html', {'all_events': all_events})

@login_required
def open_positions(request):
    unfilled = Schedule.objects.filter(user__isnull = True).order_by('date', 'time')
    return render(request, 'open_positions.html', {'unfilled': unfilled})

@login_required
def profile_view(request):
    user = request.user
    edit_field = request.GET.get('edit', None)

    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value')

        if field in ['first_name', 'last_name', 'email']:
            setattr(user, field, value)
            user.save()
            messages.success(request, f"{field.replace('_', ' ').title()} updated.")
            return redirect('profile')

        form = UserUpdateForm(request.POST, instance = user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

    else:
        form = UserUpdateForm(instance = user)

    return render(request, 'profile.html', {'user': user, 'edit_field': edit_field, 'form': form})

@staff_member_required
def manage_roles(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')

        try:
            user = User.objects.get(id = user_id)

            if new_role == 'staff':
                user.is_staff = True
                user.is_superuser = False

            elif new_role == 'superuser':
                user.is_staff = True
                user.is_superuser = True

            else:
                user.is_staff = False
                user.is_superuser = False

            user.save()
            messages.success(request, f"Updated role for {user.username}")

        except User.DoesNotExist:
            messages.error(request, "User not found.")

    users = User.objects.all().order_by('username')
    return render(request, 'manage_roles.html', {'users': users})