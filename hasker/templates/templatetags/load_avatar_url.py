from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def load_avatar_url(user):
    if user and user.avatar:
        return user.avatar.url
    return settings.DEFAULT_AVATAR_URL

