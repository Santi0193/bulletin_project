from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment

SITE_URL = 'http://127.0.0.1:8000'


@receiver(post_save, sender=Comment)
def comment_created(instance, created, **kwargs):
    if not created:
        return

    email = User.objects.filter(post__id=instance.post_id).values_list('email', flat=True)

    subject = f'На ваше объявление поступил новый отклик!'

    text_content = (
        f'Заголовок вашего объявления: {instance.post.heading}\n'
        f'Текст вашего объявления: {instance.post.text}\n'
        f'Автор отклика: {instance.user}\n'
        f'Текст отклика: {instance.text}\n\n'
        f'Ссылка на объявление: {SITE_URL}{instance.get_absolute_url()}'
    )
    html_content = (
        f'Заголовок вашего объявления: {instance.post.heading}<br>'
        f'Текст вашего объявления: {instance.post.text}<br>'
        f'Автор отклика: {instance.user}<br>'
        f'Текст отклика: {instance.text}<br><br>'
        f'<a href="{SITE_URL}{instance.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )

    msg = EmailMultiAlternatives(subject, text_content, None, email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Comment)
def review_accepted(instance, **kwargs):
    if instance.status:
        email = instance.user.email

        subject = f'Ваш отклик был принят!'

        text_content = (
            f'Текст вашего отклика: {instance.text}\n'
            f'Ссылка на объявление: {SITE_URL}{instance.get_absolute_url()}'
        )
        html_content = (
            f'Текст вашего отклика: {instance.text}<br>'
            f'<a href="{SITE_URL}{instance.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
        )

        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Comment)
def review_rejected(instance, created, **kwargs):
    if not created:
        if not instance.status:
            email = instance.user.email

            subject = f'Ваш отклик был отклонен!'

            text_content = (
                f'Текст вашего отклика: {instance.text}\n'
                f'Ссылка на объявление: {SITE_URL}{instance.get_absolute_url()}'
            )
            html_content = (
                f'Текст вашего отклика: {instance.text}<br>'
                f'<a href="{SITE_URL}{instance.get_absolute_url()}">'
                f'Ссылка на объявление</a>'
            )

            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
