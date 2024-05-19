from django.shortcuts import render, HttpResponse ,HttpResponseRedirect
from website.models import *
from website.forms import ContactForm , NewsletterForm


# Create your views here.
def index_view(request):
    return render(request, 'website/index.html')


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
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
            email = request.POST.get('email')
            Newsletter.objects.create(email=email)
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
