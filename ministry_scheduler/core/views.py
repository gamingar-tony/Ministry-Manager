from .forms import CustomUserCreationForm, UserUpdateForm, HomilyForm, NoteForm
from .models import ScheduleEntry, Schedule, Homily, Note
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

@login_required
def settings_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        email_notifications = request.POST.get('email_notifications') == 'on'
        dark_mode = request.POST.get('dark_mode') == 'on'

        profile.email_notifications = email_notifications
        profile.dark_mode = dark_mode
        profile.save()

        messages.success(request, 'Settings saved.')
        return redirect('settings')

    return render(request, 'settings.html', {'profile': profile})

@login_required
def homily_import_view(request):
    if request.method == 'POST':
        form = HomilyForm(request.POST, request.FILES)

        if form.is_valid():
            homily = form.save(commit = False)
            homily.uploaded_by = request.user
            homily.save()
            return redirect('homily_import')

    else:
        form = HomilyForm()

    homilies = Homily.objects.order_by('-date')
    return render(request, 'homily_import.html', {'form': form, 'homilies': homilies})

@login_required
def notes_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit = False)
            note.created_by = request.user
            note.save()
            return redirect('notes')

    else:
        form = NoteForm()

    my_notes = Note.objects.filter(created_by = request.user)
    shared_notes = Note.objects.filter(is_public = True).exclude(created_by = request.user)

    return render(request, 'notes.html', {'form': form, 'my_notes': my_notes, 'shared_notes': shared_notes})