from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def check(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        messages.error(request, "Site You Requested: " + url+ " is a Phishing Website")
    return redirect('/')