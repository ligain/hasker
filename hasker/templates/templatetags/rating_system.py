from django import template

register = template.Library()


@register.simple_tag
def voted_class(user, obj, direction):
    user_vote = obj.votes.filter(author=user).first()
    if user_vote:
        if user_vote.value == direction:
            return 'text-primary'