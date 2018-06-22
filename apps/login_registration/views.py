from django.shortcuts import render, redirect, HttpResponse
from apps.login_registration.models import *
from djangounchained_flash import ErrorManager, getFromSession
import bcrypt
from . import customHash

def index(request):
    if 'flash' not in request.session:
        request.session['flash']=ErrorManager().addToSession()
    if 'loggedIn' not in request.session:
        request.session['loggedIn']=False
    if 'userID' not in request.session:
        request.session['userID']=-1
        request.session['systemCheck']=-1
    if request.session['loggedIn']==True:
        return redirect('/login/')
    if 'fName' not in request.session:
        request.session['fName']=''
        request.session['lName']=''
        request.session['reg_email']=''
        request.session['birthday']=''
    if 'remember' not in request.session:
        request.session['remember']=''
    if 'log_em' not in request.session:
        request.session['log_em']=''
    if request.session['loggedIn']==True:
        return redirect('/login')
    e=getFromSession(request.session['flash'])
    context={
        'reg_fName':e.getMessages('first_name'),
        'reg_lName':e.getMessages('last_name'),
        'reg_email':e.getMessages('reg_email'),
        'birthday':e.getMessages('birthday'),
        'reg_pw':e.getMessages('reg_password'),
        'confirm':e.getMessages('confirm'),
        'reg_success':e.getMessages('reg_success'),
        'login_email':e.getMessages('login_email'),
        'login_main':e.getMessages('login_main'),

        'fName':request.session['fName'],
        'lName':request.session['lName'],
        'rem_email':request.session['reg_email'],
        'bday':request.session['birthday'],
        'checked':request.session['remember'],
        'log_em':request.session['log_em'],
    }
    request.session['flash']=e.addToSession()
    return render(request, 'login_registration/loginRegistration.html', context)

def processRegister(request):
    if(request.method!='POST'):
        print('Hacker ALERT')
        return redirect('/')
    print('Attempting register')
    errors=User.objects.validate_register(request.POST)
    e=getFromSession(request.session['flash'])
    if(len(errors)):
        request.session['fName']=request.POST['first_name']
        request.session['lName']=request.POST['last_name']
        request.session['reg_email']=request.POST['reg_email']
        request.session['birthday']=request.POST['birthday']
        for tag, error in errors.items():
            e.addMessage(error, tag)
        request.session['flash']=e.addToSession()
        return redirect('/')
    hashedPW=bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['reg_email'], birthday=request.POST['birthday'], password=hashedPW)
    e.addMessage('Successfully registered', 'reg_success')
    remember=request.session['remember']
    log_em=request.session['log_em']
    request.session.clear()
    request.session['remember']=remember
    request.session['log_em']=log_em
    request.session['flash']=e.addToSession()
    return redirect('/')

def processLogin(request):
    if(request.method!='POST'):
        print('Hacker ALERT')
        return redirect('/')
    print('Attempting to log in')
    errors=User.objects.validate_login(request.POST)
    e=getFromSession(request.session['flash'])
    if(len(errors)):
        for tag,error in errors.items():
            e.addMessage(error, tag)
        request.session['flash']=e.addToSession()
        return redirect('/')
    print('Login attempt successful')
    request.session['loggedIn']=True
    if 'remember_me' in request.POST:
        print('Remembering user')
        request.session['log_em']=request.POST['login_email']
        request.session['remember']='checked'
    else:
        request.session['log_em']=''
        request.session['remember']=''
    this_user=User.objects.get(email=request.POST['login_email'])
    request.session['userID']=this_user.id
    request.session['systemCheck']=customHash.createHash(str(this_user.created_at))
    return redirect('/login/')

def login(request):
    if(request.session['loggedIn']==False):
        return redirect('/')
    if(customHash.compare(str(User.objects.get(id=request.session['userID']).created_at), request.session['systemCheck'])==False):
        print('Someone is attempting to mess with the database by changing their user id.')
        print('Defense mode activated')
        request.session.clear()
        return HttpResponse('You are attempting to do illegal activities. Your IP address has been reported to the site administrator.')
    context={
        'first_name':User.objects.get(id=request.session['userID']).first_name
    }
    return redirect('/wall')
    # return render(request, 'login_registration/loginSuccess.html', context)

def logout(request):
    if(request.session['loggedIn']==False):
        return redirect('/')
    # request.session['loggedIn']=False
    remember=request.session['remember']
    log_em=request.session['log_em']
    request.session.clear()
    request.session['remember']=remember
    request.session['log_em']=log_em
    print('Successfully logged out')
    return redirect('/')