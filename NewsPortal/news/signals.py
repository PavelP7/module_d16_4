from django.db.models.signals import m2m_changed
from .models import PostCategory, Category
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from NewsPortal.settings import *
from .tasks import send_post

def send_created_post(user, post):
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

@receiver(m2m_changed, sender=PostCategory)
def notify_about_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        for category in categories:
            users = category.subscribers.all()
            for user in users:
                # send_created_post(user, instance)
                send_post.apply_async([user.id, instance.id])

