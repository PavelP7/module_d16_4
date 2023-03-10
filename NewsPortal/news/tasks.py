from .models import Post, Category, User
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from NewsPortal.settings import *

def periodic_mails_send():
    posts_list = {}
    last_week = datetime.now() - timedelta(weeks=1)

    for user in User.objects.all():
        for category in Category.objects.filter(subscribers=user):
            posts = list(Post.objects.filter(category=category, datetime_in__gte=last_week).values())
            if user in posts_list.keys():
                posts_list[user].append(posts)
            else:
                posts_list[user] = posts

    for user in posts_list.keys():
        html_content = render_to_string(
            'mail_form_list.html',
            {
                'username': user.username,
                'posts': posts_list[user],
            }
        )

        msg = EmailMultiAlternatives(
            subject=f"Подборка статей за прошедшую неделю",
            to=[f'{user.email}'],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

@shared_task
def send_post(user_id, post_id):
    user = User.objects.get(pk=user_id)
    post = Post.objects.get(pk=post_id)

    html_content = render_to_string(
        'mail_form.html',
        {
            'username': user.username,
            'post': post,
            'link': f'{SITE_URL}/news/{post.id}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=f"{post.title}",
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=[f'{user.email}'],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def periodic_mails():
    periodic_mails_send()
