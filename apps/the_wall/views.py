from django.shortcuts import render, redirect, HttpResponse
from apps.the_wall.models import *
from apps.login_registration.models import *
from djangounchained_flash import ErrorManager, getFromSession

def index(request):
    if 'loggedIn' not in request.session:
        request.session['loggedIn']=False
    if request.session['loggedIn']==False:
        return redirect('/')
    if 'flash' not in request.session:
        request.session['flash']=ErrorManager().addToSession()
    if 'post_failID' not in request.session:
        request.session['post_failID']=-1
    if 'post_goodID' not in request.session:
        request.session['post_goodID']=-1
    e=getFromSession(request.session['flash'])
    context={
        'post_success':e.getMessages('post_success'),
        'post_fail':e.getMessages('post_fail'),
        'posts':Post.objects.all().order_by('-created_at'),
        'comment_fail':e.getMessages('comment_fail'),
        'post_failID':int(request.session['post_failID']),
        'comment_success':e.getMessages('comment_success'),
        'post_goodID':request.session['post_goodID'],
        'first_name':User.objects.get(id=int(request.session['userID'])).first_name
    }
    request.session['flash']=e.addToSession()
    return render(request, 'the_wall/wall.html', context)

def processPost(request):
    if request.method!='POST':
        print('Hack attempted')
        return redirect('/wall')
    errors=Post.objects.validate(request.POST)
    e=getFromSession(request.session['flash'])
    if(len(errors)):
        for tag, error in errors.items():
            e.addMessage(error, tag)
        request.session['flash']=e.addToSession()
        return redirect('/wall')
    e.addMessage('Successfully posted', 'post_success')
    request.session['flash']=e.addToSession()
    Post.objects.create(content=request.POST['message'], sender_id=User.objects.get(id=request.session['userID']))
    print('Processing new post')
    return redirect('/wall')

def processComment(request, post_id):
    if request.method!='POST' or len(Post.objects.filter(id=post_id))==0:
        print('Hack attempted')
        return redirect('/wall/')
    errors=Comment.objects.validate(request.POST)
    e=getFromSession(request.session['flash'])
    if len(errors):
        for tag, error in errors.items():
            e.addMessage(error, tag)
        request.session['post_failID']=post_id
        request.session['post_goodID']=-1
        request.session['flash']=e.addToSession()
        return redirect('/wall')
    request.session['post_failID']=-1
    Comment.objects.create(content=request.POST['comment'], posted_to=Post.objects.get(id=int(post_id)), sender_id=User.objects.get(id=request.session['userID']))
    e.addMessage('Successfully commented', 'comment_success')
    request.session['flash']=e.addToSession()
    request.session['post_goodID']=int(post_id)
    print('Adding new comment')
    return redirect('/wall')

def getComments(request, post_id):
    if request.method != 'POST':
        print('Invalid entry attempted')
        return redirect('/')
    print('Getting request for comments for post: ',post_id)
    context={
        'comments':Post.objects.get(id=int(post_id)).comments.all()
    }
    return render(request, 'the_wall/comments.html', context)
# Create your views here.
