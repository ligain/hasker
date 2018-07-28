from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def load_avatar_url(context):
    if context['user'].profile.avatar:
        return context['user'].profile.avatar.url
    else:
        return settings.DEFAULT_AVATAR_URL

