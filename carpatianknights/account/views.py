from django.shortcuts import render
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import register_user, registration_user_to_tour, get_dashboard_context


def registration_user_view(request):
    if request.method == 'POST':
        register_user(request)
    else:
        context = {
            'user_form': UserRegistrationForm(),
        }
        return render(request, 'account/register.html', context=context)


@login_required
def dashboard_view(request):
    if request.method == 'POST':
        registration_user_to_tour(request)
    context = get_dashboard_context(request.user)
    return render(request, 'account/dashboard.html', context)


@login_required
def edit_user_profile_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профіль успішно змінений')
        else:
            messages.error(request, 'Помилка зміни профілю')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})
