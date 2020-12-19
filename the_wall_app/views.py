import bcrypt
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import *


def index(request):
    return render(request, 'index.html')


def register_user(request):

    errors = Users.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt() 
        ).decode() 
    
        print(hash_browns)
    
        created_user = Users.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            hashed_password=hash_browns,
        )
        request.session['emailid'] = created_user.id

        return redirect('/wall')


def login_user(request):
    errors = Users.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = Users.objects.get(email=request.POST['email'])
        request.session['emailid'] = user.id
        print(request.session['emailid'])
        return redirect('/wall')


def show_wall(request):
    if 'emailid' not in request.session:
        return redirect('/')
    context = {
        'user_logged_in': Users.objects.get(id=request.session['emailid']),
        'posts' : Messages.objects.all(),
    }
    return render(request, 'wall.html', context)

def create_a_post(request):
    Messages.objects.create(
        message=request.POST['message'], 
        message_poster = Users.objects.get(id=request.session['emailid']))
    return redirect('/wall')
    
def post_a_comment(request):
    Comments.objects.create(
        comment=request.POST['comment'], 
        messages_comments = Users.objects.get(id=request.session['emailid']), 
        posting_comment = Messages.objects.get(id=request.POST['posting_comment_id']))
    return redirect('/wall')

def delete_message(request, id):
    Messages.objects.get(id=id).delete()
    return redirect('/wall')

def delete_comment(request, id):
    Comments.objects.get(id=id).delete()
    return redirect('/wall')

def logout_user(request):
    del request.session['emailid']
    return redirect('/')




