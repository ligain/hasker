from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from hasker.core.models import Question


def trending(request):
    return {
        'trending_questions': Question.objects.annotate(
                votes_rating=Coalesce(Sum('votes__value'), Value(0))
            ).order_by('-votes_rating')[:20]
    }