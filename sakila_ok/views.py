#coding: utf8

from django.shortcuts import render

# Urls and HttpResponses
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response

# # User forms
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User, Permission
# from yalladevelop.forms import *
# from django.utils.html import escape

# # Authentication and Users
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required, permission_required
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.core.context_processors import csrf
# from django.template import RequestContext

# Models
from sakila_ok.models import *
from django.db.models import *

# # Mailer
# from django.core.mail import send_mail

# # Paginator
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# # Other Imports
# import random
# from django.conf.urls import patterns, url

# # Image Handlers
# from base64 import b64decode
# from django.core.files.base import ContentFile

# -------------------- Parameters Function -------------------------
# Function returns a dictionary of the variables
def getVariables(request,dictionary={}):
    if dictionary:
        return dictionary
    else:
        return {}

def error404(request):
    return render(request, 'sakila_ok/404.html', {})

def error500(request):
    return render(request, 'sakila_ok/500.html', {})

def getStatus(customer_id):
    # try:
        # Customer.objects.get(id=customer_id) # check if the customer exists
    # except Exception:
        # return None # return None if not found
    cursor = connection.cursor() # opening a cursor to execute MySQL commands
    cursor.callproc('sakila.CustomerStatus',[customer_id]) # calling the procedure
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    return tmp[0][0] # parsing the results & returning it

def getCustomerBalance(cus_id):
    if type(cus_id) != str:
        cus_id = str(cus_id)
    cursor = connection.cursor()
    query = "SELECT totalBalanceDue(%i);" % int(cus_id)
    result = cursor.execute(query)
    result2 = cursor.fetchone()[0]
    cursor.close()
    return result2

def pay(request, cus_id):
    cursor = connection.cursor()
    cursor.callproc('sakila.payBalance',[cus_id])
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    return customer(request, cus_id, alert="Something happened")

def get_movie_status3(film_id):
    count = Film.objects.count()
    limit = int(count * .2)

    cursor = connection.cursor()
    cursor.execute("SELECT film_id from allMovies;")
    total_rows = cursor.fetchall()

    top10 = total_rows[:10]
    hot = total_rows[10:limit]
    # regular = total_rows[limit:1000-limit]
    dud = total_rows[count - limit:]

    top10_l = []
    hot_l = []
    dud_l = []

    for i in top10:
        top10_l.append(i[0])
        print i
    for i in hot:
        hot_l.append(i[0])
    for i in dud:
        dud_l.append(i[0])

    if film_id in top10_l:
        return "Top 10"
    elif film_id in hot_l:
        return "Hot"
    elif film_id in dud_l:
        return "Dud"
    else:
        return "Regular"

def get_customer_status(cus_id):
    count = Customer.objects.count()
    limit = int(count * .2)

    cursor = connection.cursor()
    cursor.execute("SELECT customer_id FROM sakila.allCustomers;")
    total_rows = cursor.fetchall()

    preferred = total_rows[:limit]
    casual = total_rows[count - limit:]

    p = []
    c = []

    for i in preferred:
        p.append(i[0])
    for i in casual:
        c.append(i[0])

    if cus_id in p:
        return "Preferred"
    elif cus_id in c:
        return "Casual"
    else:
        return "Regular"

def get_last_5(customer_id):
    cursor = connection.cursor() # opening a cursor to execute MySQL commands
    cursor.callproc('sakila.last5', [customer_id]) # calling the procedure
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    if len(tmp) > 1:
        return tmp
    else:
        return None

def get_inventory(film_id):
    cursor = connection.cursor() # opening a cursor to execute MySQL commands
    cursor.callproc('sakila.Instore', [film_id]) # calling the procedure
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    if len(tmp) > 1:
        return tmp
    else:
        return None

def get_inventory2(film_id):
    cursor = connection.cursor() # opening a cursor to execute MySQL commands
    cursor.callproc('sakila.Alltogether', [film_id]) # calling the procedure
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    if len(tmp) > 1:
        return tmp
    else:
        return None

def get_rentedout(film_id):
    cursor = connection.cursor() # opening a cursor to execute MySQL commands
    cursor.callproc('sakila.Rentedout', [film_id]) # calling the procedure
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    if len(tmp) > 1:
        return tmp
    else:
        return None

def get_actors(film_id):
    cursor = connection.cursor() # opening a cursor to execute MySQL commands
    cursor.callproc('sakila.Movieinfo', [film_id]) # calling the procedure
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    if len(tmp) > 1:
        return tmp
    else:
        return None

# def get_movie_status2(film_id):
#     cursor = connection.cursor() # opening a cursor to execute MySQL commands
#     cursor.callproc('sakila.MovieStatus2', [film_id]) # calling the procedure
#     tmp = cursor.fetchall() # fetching results
#     cursor.close() # closing the cursor connection
#     if len(tmp) >= 1:
#         return tmp[0][0]
#     else:
#         return None

def get_last_5_rentals(film_id):
    cursor = connection.cursor() # opening a cursor to execute MySQL commands
    cursor.callproc('sakila.last5rentals', [film_id]) # calling the procedure
    tmp = cursor.fetchall() # fetching results
    cursor.close() # closing the cursor connection
    if len(tmp) > 1:
        return tmp
    else:
        return None


def home(request):
    d = getVariables(request, dictionary={'page_name': "Home"})
    # if Staff.objects.all():
    #     d['first_staff'] = Staff.objects.all()[0] # < SQL QUERY HERE IN PYTHON!!
    # if Category.objects.all():
    #     d['all_categories'] = Category.objects.all()
    # if Customer.objects.all():
    #     customer = Customer.objects.all()[0]
    #     d['customer'] = customer
    #     d['cust_status'] = getStatus(customer.customer_id)
    return render(request, 'sakila_ok/index.html', d)

def category(request, cat_id=None):
    d = getVariables(request,dictionary={'page_name': "Category"})
    if Category.objects.all():
        try:
            x = Category.objects.get(category_id=cat_id)
            d['x'] = x.name
        except Exception:
            d['x'] = "Not Found"
    return render(request, 'sakila_ok/index.html', d)

def customer(request, cus_id=None, alert=None):
    d = getVariables(request,dictionary={'page_name': "Customer"})
    if not cus_id:
        d['c_all'] = Customer.objects.all()
    else:
        # individual customer page 
        if alert:
            d['alert'] = alert
        d['c_all'] = None
        c = Customer.objects.get(customer_id=cus_id)
        d['c'] = c
        d['cust_status'] = get_customer_status(int(cus_id))
        d['last5'] = get_last_5(cus_id)
        d['balance_due'] = getCustomerBalance(cus_id)
        d['pay_history'] = Payment.objects.filter(customer=c.customer_id).order_by('-payment_date')

        
    return render(request, 'sakila_ok/customer.html', d)

def film(request, film_id=None):
    d = getVariables(request,dictionary={'page_name': "Films"})
    if not film_id:
        d['f_all'] = Film.objects.all()
    else:
        f = Film.objects.get(film_id=film_id)
        d['f_language'] = f.language.name
        d['f'] = f
        d['inventory'] = get_inventory(film_id)
        d['rented_out'] = get_rentedout(film_id)
        d['actors'] = get_actors(film_id)
        d['recent_rentals'] = get_last_5_rentals(film_id)
        d['m_status'] = get_movie_status3(int(film_id))

    return render(request, 'sakila_ok/film.html', d)

def film_search(request):
    d = getVariables(request, dictionary={'page_name': "Search"})
    if request.method == 'GET':
        if request.GET['id'] == 'error':
            d['error'] = True
            return render(request, 'sakila_ok/film_search.html', d)

        try:
            film_id = request.GET['id']
            d['req'] = film_id
        except Exception:
            d['error'] = True
            return render(request, 'sakila_ok/film_search.html', d)
        
        try:
            film_id = request.GET['id']
            the_film_id = int(film_id)

        except Exception:
            the_film_id = None
            film_id = film_id.upper()

        if type(the_film_id) == int:
            film_ids = Film.objects.filter(film_id=the_film_id)
            if film_ids:
                d['film_ids'] = film_ids[0]
        else:
            d['film_ids'] = None
        d['films'] = Film.objects.filter(title__contains=film_id)

    else:
        d['error'] = True
    return render(request, 'sakila_ok/film_search.html', d)

def cap(request, cus_id=None, film_id=None):
    d = getVariables(request, dictionary={'page_name': "Checkout & Pay"})

    return render(request, 'sakila_ok/checkout-and-pay.html', d)
