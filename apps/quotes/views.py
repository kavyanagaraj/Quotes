from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages
from django.core.urlresolvers import reverse
import bcrypt, datetime, time
from datetime import datetime


def index(request):
    return render(request, "index.html")

def quotes(request):
    context = {
    "user" : User.objects.get(id = request.session['uid']),
    "quotes" : Quote.objects.all()
    }
    return render(request, "quotes.html", context)

def userwall(request, id):
    user = User.objects.get(id = id)
    context = {
    "user" : User.objects.get(id = id),
    "quotes" : Quote.objects.filter(postedby = user)
    }
    return render(request, "userquotes.html", context)

def postquote(request):
    user = User.objects.get(id = request.session['uid'])
    quote = request.POST['quote']
    quotedby = request.POST['quotedby']
    context = {
    "quote" : quote,
    "quotedby" : quotedby
    }
    error = Quote.objects.validatequote(context)
    if error:
        for ele in error:
            messages.add_message(request, messages.ERROR, ele)
        return redirect('/quotes')
    else:
        Quote.objects.create(quote = quote, postedby = user, quotedby = quotedby)
    return redirect('/quotes')

def favquote(request, id):
    quote = Quote.objects.get(id = id)
    user = User.objects.get(id = request.session['uid'])
    quote.faves.add(user)
    return redirect('/quotes')

def removefavquote(request, id):
    quote = Quote.objects.get(id = id)
    user = User.objects.get(id = request.session['uid'])
    quote.faves.remove(user)
    return redirect('/quotes')

def register(request):
    request.session['login'] = False
    fname = str(request.POST['first_name'])
    lname = str(request.POST['last_name'])
    email = str(request.POST['email'])
    bday = request.POST['bday'].encode()
    pwd = request.POST['password'].encode()
    conpwd = request.POST['confirm_password'].encode()
    context = {
    "fname" : fname,
    "lname" : lname,
    "email" : email,
    "bday" : bday,
    "pwd" : pwd,
    "conpwd" : conpwd
    }
    if  User.objects.all().filter(email = email):
        messages.add_message(request, messages.INFO, "Email already exists! Please login")
        return redirect('/')
    error = User.objects.validate(context)
    if error:
        for ele in error:
            messages.add_message(request, messages.ERROR, ele)
        return redirect('/')
    else:
        hashedpwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
        user = User.objects.create(first_name = fname, last_name = lname, email = email, password = hashedpwd, birthday = bday)
        request.session['uid'] = user.id
        return redirect('/quotes')

def login(request):
    request.session['login'] = True
    email = str(request.POST['email'])
    pwd = request.POST['password'].encode()
    user = User.objects.all().filter(email = email)
    if  not user:
        messages.add_message(request, messages.INFO, "Email doesn't exist! Please register")
        return redirect('/')
    else:
        if user[0].password != bcrypt.hashpw(pwd, (user[0].password).encode()):
            messages.add_message(request, messages.INFO, "Invalid password")
            return redirect('/')
        else:
            request.session['uid'] = user[0].id
            return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/')
