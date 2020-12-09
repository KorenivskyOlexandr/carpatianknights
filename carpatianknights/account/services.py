from django.shortcuts import render
from .forms import UserRegistrationForm, TourRegistrationForm
from .models import Profile
from carpatianknights.route.models import Tour, ActiveRoute
from django.contrib import messages
from django.db import IntegrityError
from datetime import date
from django.core.validators import ValidationError


def register_user(request):
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.username = new_user.email
        date_of_birth = date(year=int(request.POST.get("date_of_birth_year")),
                             month=int(request.POST.get("date_of_birth_month")),
                             day=int(request.POST.get("date_of_birth_day")))
        new_profile = Profile(user=new_user, phone_number=request.POST.get(
            "phone_number"), date_of_birth=date_of_birth)
        try:
            new_user.clean()
            new_profile.clean()
            new_user.save()
            new_profile.save()
        except ValidationError:
            messages.error(request, "Обмеження по віку 16+, або супровід батьків")
            return render(request, 'account/register.html', {'user_form': UserRegistrationForm()})
        except IntegrityError:
            messages.error(request, "Корисутвач з таким номером телефону вже стоврений")
            return render(request, 'account/register.html', {'user_form': UserRegistrationForm()})

        return render(request,
                      'account/register_done.html',
                      {'new_user': new_user})
    if 'email' in user_form.errors:
        messages.error(request, "Користувач з таким email вже створений")
        return render(request, 'account/register.html', {'user_form': UserRegistrationForm()})


def registration_user_to_tour(request):
    tour_registration_form = TourRegistrationForm(request.POST)
    if tour_registration_form.is_valid():
        cd = tour_registration_form.cleaned_data
        tour = Tour(user_id=request.user, active_route_id=get_active_tour(cd['active_tours'].id))
        try:
            tour.save()
            messages.success(
                request, 'Заявку подано успішно подано, глава походу зв\'яжеться з вами')
        except IntegrityError:
            messages.error(request, 'Ви вже подавали заявку на цей тур')


def get_dashboard_context(user):
    return {'section': 'dashboard',
            'tour_registration_form': TourRegistrationForm(),
            'user_active_tour': get_user_active_tour(user.id),
            'user_history_tour': get_user_history_tour(user.id),
            'user': user}


def get_user_active_tour(user_id):
    return Tour.objects.all().filter(user_id=user_id, active_route_id__status=True)


def get_user_history_tour(user_id):
    return Tour.objects.all().filter(user_id=user_id, active_route_id__status=False)


def get_active_tour(active_tour_id):
    return ActiveRoute.objects.get(id=active_tour_id)
