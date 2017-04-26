from __future__ import unicode_literals
from django.db import models
import re
import datetime, time
from datetime import datetime

class UserManager(models.Manager):
    def validate(self, data):
        error = []
        emailreg = '[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+'
        if len(data['fname']) < 2 or not str.isalpha(data['fname']):
            error.append("Invalid First Name")
        if len(data['lname']) < 2 or not str.isalpha(data['lname']):
            error.append("Invalid Last Name")
        if  not re.search(emailreg, data['email']):
            error.append("Invalid Email")
        if len(data['pwd']) < 4:
            error.append("Minimum of 8 characters required for password")
        if data['pwd'] != data['conpwd']:
            error.append("Password doesn't match")
        if not data['bday']:
            error.append("Please enter a valid date")
        return error

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length= 255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday=models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def validatequote(self, data):
        error = []
        if len(data['quotedby']) < 3:
            error.append("* Minimum 3 characters required")
        if len(data['quote']) < 10:
            error.append("* Minimum 10 characters required to quote")
        return error

class Quote(models.Model):
    quote = models.TextField()
    quotedby = models.CharField(max_length = 255)
    postedby = models.ForeignKey(User, related_name = "user_quote")
    faves = models.ManyToManyField(User, related_name = "favquote")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
