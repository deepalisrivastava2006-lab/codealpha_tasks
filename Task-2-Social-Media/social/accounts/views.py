from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return HttpResponse("""
        <h1>Welcome to CodeAlpha Social Media</h1>
        <p>Your social media platform is under development.</p>
    """)
