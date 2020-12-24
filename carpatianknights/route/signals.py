from django.core.exceptions import ValidationError
from django.db.models import signals
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .models import Tour
from django.conf import settings


@receiver(signals.post_save, sender=Tour)
def notify_admin(instance, created, **kwargs):
    """Сповіщення адмінів про реєстрацію користувача на похід"""
    if created:
        user = instance.user_id
        active_route = instance.active_route_id
        html_message = render_to_string('admin.html', {'route': active_route.routes_id,
                                                       'start_day': active_route.start_day,
                                                       'stop_day': active_route.stop_day,
                                                       'leader': active_route.leader,
                                                       'full_name': user.get_full_name(),
                                                       'phone': user.profile.phone_number,
                                                       'age': user.profile.date_of_birth,
                                                       'email': user.email,
                                                       'url': settings.SERVER,
                                                       'tour_id': instance.id
                                                       })
        plain_message = strip_tags(html_message)
        send_mail(
            subject='Карпатські Відчайдухи',
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['carpatianknights@ukr.net', 's5a5s5h5a5@ukr.net'],
            html_message=html_message,
            fail_silently=False,
        )


@receiver(signals.pre_save, sender=Tour)
def notify_users(instance, **kwargs):
    """Сповіщення юзера про те що його прийнято в похід,
        а також збільшення/зменшення кількості вільних місць в поході"""
    status = False
    try:
        tour = Tour.objects.get(id=instance.id)
        status = tour.status
    except Exception:
        pass
    if instance.status != status:
        if instance.status:
            user = instance.user_id
            active_route = instance.active_route_id
            if active_route.is_full:
                raise ValidationError(
                    "Похід немає вільних місць")
            else:
                active_route.add_user()
                sent_user_mail(user, active_route)
        else:
            instance.active_route_id.remove_user()


@receiver(signals.post_delete, sender=Tour)
def remove_user(instance, **kwargs):
    instance.active_route_id.remove_user()


def sent_user_mail(user, active_route):
    html_message = render_to_string('mail.html', {'route': active_route.routes_id,
                                                  'start_day': active_route.start_day,
                                                  'stop_day': active_route.stop_day,
                                                  'leader': active_route.leader,
                                                  'url': settings.SERVER  # ! change url !
                                                  })
    plain_message = strip_tags(html_message)
    send_mail(
        subject='Карпатські Відчайдухи',
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
