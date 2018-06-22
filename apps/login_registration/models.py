from __future__ import unicode_literals
from django.db import models
import re
from datetime import date
import bcrypt

class UserManager(models.Manager):
    def calculateAge(self,birthday):
        today=date.today()
        birthYear=int(birthday[0:4])
        birthMonth=int(birthday[5:7])
        birthDate=int(birthday[8:10])
        return today.year - birthYear - ((today.month, today.day) < (birthMonth, birthDate))

    def validate_register(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postData['first_name'])<2:
            errors['first_name']='First name cannot empty'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name cannot be empty'
        if len(postData['reg_email'])<5:
            errors['reg_email']='Email address invalid'
        elif not EMAIL_REGEX.match(postData['reg_email']):
            errors['reg_email']='Email address invalid'
        elif(len(User.objects.filter(email=postData['reg_email']))==1):
            errors['reg_email']='An account is already registered to that email'
        if(len(postData['birthday'])==0):
            errors['birthday']='Invalid date of birth'
        elif(self.calculateAge(postData['birthday'])<13):
            errors['birthday']='You must be atleast 13 years old to register'
        if(len(postData['reg_password'])<8):
            errors['reg_password']='Password must be atleast 8 characters in length'
        elif(postData['reg_password']!=postData['confirm']):
            errors['confirm']='Passwords do not match'
        return errors
    
    def validate_login(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        validEmail=True
        if len(postData['login_email'])==0:
            errors['login_email']='Email cannot be empty'
            validEmail=False
        elif not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email']='Not a valid email address'
            validEmail=False
        if(validEmail==True):
            user_list=User.objects.filter(email=postData['login_email'])
            if(len(user_list)==0):
                errors['login_main']='Login attempt failed'
            else:
                user=user_list[0]
                b=bcrypt.checkpw(postData['login_password'].encode(), user.password.encode())
                print('Bcrypt compare result: ', b)
                if(b==False):
                    errors['login_main']='Login attempt failed'
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    birthday=models.DateField()
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    objects=UserManager()
# Create your models here.
