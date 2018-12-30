from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages


# Create your views here.

def handler404(request):
    return render(request, 'main_site/404.html', status=404)


def handler500(request):
    return render(request, 'main_site/500.html', status=500)



def index(request):
    #show feed template if request user is logged in
    if request.user.is_authenticated:
        # posts = Post.objects.all().order_by('-date_posted')
        # no_of_posts = len(posts)
        # context = {
        #     'posts':posts,
        #     'no_of_posts':no_of_posts,
        # }
        # return render(request, 'Post/feed.html', context)


        return redirect('feed')

    #show this template if request user is not logged in
    return render(request, 'main_site/index.html', {})

def about(request):
    return render(request, 'main_site/about.html', {})

def contact(request):
    if request.method == 'POST':
        c = Contact()
        c.name = request.POST.get('name')
        c.email = request.POST.get('email')
        c.phone = request.POST.get('phone')
        c.subject = request.POST.get('subject')
        c.message = request.POST.get('message')
        c.save()
        messages.success(request, f'Hey, your message has been received succesfully!')
        return redirect('contact')
    else:
        return render(request, 'main_site/contact.html', {})