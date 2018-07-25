from django.shortcuts import render
from django.http import HttpResponse


def main_page(request):
    # return HttpResponse("Here's the text of the Web page.")
    return render(request, 'core/main_page.html')
