from django.shortcuts import render, HttpResponse ,HttpResponseRedirect
from website.models import *
from website.forms import ContactForm , NewsletterForm
from django.contrib import messages

# Create your views here.
def index_view(request):
    return render(request, 'website/index.html')


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = "unknown"
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your ticket submitted successfully.')

        else:
            messages.add_message(request, messages.ERROR, 'your ticket didnt submitted')

    form = ContactForm()
    return render(request, 'website/contact.html', {'form': form})
# def test(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('Your message is sent successfully!')
#         else:
#             return HttpResponse('Your message isnt sent successfully!')
#     form = ContactForm()
#     return render(request,'test.html',{'form':form})
def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
