from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, TourRegistration
from django.contrib.auth.decorators import login_required
from .models import Profile
from carpatianknights.news.models import Tour, ActiveRoutes
from django.contrib import messages
from django.db import IntegrityError


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['email'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    if request.method == 'POST':
        tour_registration_form = TourRegistration(request.POST)
        if tour_registration_form.is_valid():
            cd = tour_registration_form.cleaned_data
            active_tour = ActiveRoutes.objects.get(id=cd['active_tours'].id)
            tour = Tour(user_id=request.user, active_route_id=active_tour)
            try:
                tour.save()
                messages.success(
                    request, 'Заявку подано успішно подано, глава походу зв\'яжеться з вами')
            except IntegrityError:
                messages.error(request, 'Ви вже подавали заявку на цей тур')
    confirm_tour = Tour.objects.all().filter(user_id=request.user.id)
    print(confirm_tour)
    context = {'section': 'dashboard',
               'tour_registration_form': TourRegistration(),
               'confirm_tour': confirm_tour}
    return render(request, 'account/dashboard.html', context)


# @login_required
# def registration_to_tour(request):
#     # print(request.user)
#     if request.method == 'POST':
#         active_tour_form = TourRegistration(request.POST)
#         if active_tour_form.is_valid():
#             cd = active_tour_form.cleaned_data
#             active_tour = ActiveRoutes.objects.get(id=cd['active_tours'].id)
#             tour = Tour(user_id=request.user, active_route_id=active_tour)
#             print(tour)
#             return HttpResponse('Authenticated successfully')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.username = new_user.email
            # Сохраняем пользователя в базе данных.
            new_user.save()
            new_profile = Profile(user=new_user, phone_number=request.POST.get(
                "phone_number"), age=request.POST.get("age"))
            new_profile.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        context = {
            'user_form': UserRegistrationForm(),
        }
    return render(request, 'account/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})
