from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def load_avatar_url(user):
    if user and user.profile.avatar:
        return user.profile.avatar.url
    return settings.DEFAULT_AVATAR_URL

