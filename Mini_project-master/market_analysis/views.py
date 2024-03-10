import heapq
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from .models import DataModel

from django.shortcuts import render
from django.contrib.auth import authenticate, login

import datetime


def index(request):
    return render(request, 'index.html')


def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('graph')
        else:
            return redirect('login')
    return render(request, 'login.html')


def graph_data(date='', today=datetime.date.today().strftime("%d-%m-%Y"), which_date='all_time'):

    result = DataModel.objects.all()

    products = {}
    products['Male'] = {
        '0-3' : 'Age : 0-3', 
        '4-9' : 'Age : 3-9',
        '10-15' : 'Age : 10-15' ,
        '16-20' : ['Age : 16-20','Apparels','School supplies and stationery'], 
        '21-30' : ['Age : 21-30','Groomig Products','Apparel and Accessories','Books and Magazines','Gaming Accessories'], 
        '31-40' : 'Age : 31-40', 
        '41-53' : 'Age : 41-53', 
        '55+' : 'Age : 55+'
    }

    products['Female'] = {
        '0-3' : 'Age : 0-3', 
        '4-9' : 'Age : 4-10',
        '10-15' : ['Age : 10-15','Books, arts, and crafts','School supplies and stationery'] ,
        '16-20' : 'Age : 16-20', 
        '21-30' : ['Age : 21-30','Beauty Products','Fashion Accessoris'], 
        '31-40' : 'Age : 31-42', 
        '41-53' : 'Age : 43-55', 
        '55+' : 'Age : 55+'
    }

    data = {}
    data['Male'] = {}
    data['Female'] = {}
    age_cat = ['0-3', '4-9', '10-15', '16-20', '21-30', '31-40', '41-53', '55+']
    male_cat,female_cat = [],[]
    count = 0

    for object in result:
        cur_date = object.date

        if len(date) < 3 and date != '':
            day,month,year = map(str,cur_date.split('-'))
            cur_date = month

        if cur_date == date or date == '':
            gender = object.gender
            age = object.age    
            count = int(object.count)

            if age in data[gender].keys():
                data[gender][age] += count
            else:
                data[gender][age] = count

    for x in age_cat:
        if x in data["Male"].keys() and x in data["Female"].keys():
            male_cat.append(data["Male"][x])
            female_cat.append(data["Female"][x])
        elif x in data["Male"].keys():
            male_cat.append(data["Male"][x])
            female_cat.append(0)
        elif x in data['Female'].keys():
            male_cat.append(0)
            female_cat.append(data["Female"][x])
        else:
            male_cat.append(0)
            female_cat.append(0)

    count = [sum(male_cat),sum(female_cat)]

    highestFemaleCat,highestMaleCat = '',''

    if len(data['Male']) > 0:
        highestMaleCat = max(data['Male'], key = data['Male'].get)
    if len(data['Female']) > 0:
        highestFemaleCat = max(data['Female'], key = data['Female'].get)

    maleProduct = '' if highestMaleCat == '' else products['Male'][highestMaleCat]
    femaleProduct = '' if highestFemaleCat == '' else products['Female'][highestFemaleCat]

    Products = maleProduct if highestMaleCat >= highestFemaleCat else femaleProduct

    maleMaxCat = heapq.nlargest(3, data['Male'].items(), key=lambda x: x[1])
    femMaxCat = heapq.nlargest(3, data['Female'].items(), key=lambda x: x[1])


    male_keys = [item[0] for item in maleMaxCat]
    male_values = [item[1] for item in maleMaxCat]

    female_keys = [item[0] for item in femMaxCat]
    female_values = [item[1] for item in femMaxCat]

    max_cat = [male_values,male_keys,female_values,female_keys]

    context = {
        'gender_count' : count,
        'age_cat' : age_cat,
        'male_cat' : male_cat,
        'female_cat' : female_cat,
        'cur_date' : today,
        'maleProduct' : maleProduct,
        'femaleProduct' : femaleProduct,
        'Products' : Products,
        'max_cat' : max_cat
    }

    return context



def graph(request):

    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    date_data = {
        'Mon' : [6,1],
        'Tue' : [5,2],
        'Wed' : [4,3],
        'Thu' : [3,4],
        'Fri' : [2,5],
        'Sat' : [1,6],
        'Sun' : [0,7]
    }
    
    today = datetime.date.today()
    cur_day = today.strftime("%a")
    month = int(today.strftime("%m"))
    year = int(today.strftime("%Y"))
    day = int(today.strftime("%d")) + date_data[cur_day][0]

    if day == 31:
        if month_days[month-1] == 30:
            day %= 10
            month += 1

    elif day > 30:
        day %= 10

        if month == 2:
            day += 2

        if month_days[month-1] == 31:
            day -= 1

        month += 1
        if month > 12:
            month = 1


    if request.method == 'POST' and 'selectedGraph' in request.POST:
        
        which_date = request.POST.get('selectedGraph')

        if which_date == 'current':
            to_day = datetime.date(year,month,day)
            date = to_day.strftime('%d-%m-%Y')
            context = graph_data(date)
            return JsonResponse(context)

        elif which_date == 'week': 
            day = int(today.strftime("%d")) - date_data[cur_day][1]

            if day <= 0:
                month -= 1
                if month_days[month-1] == 28:
                    day += 28
                elif month_days[month-1] == 30:
                    day += 30
                else:
                    day += 31

            to_day = datetime.date(year,month,day)
            date = to_day.strftime('%d-%m-%Y')
            context = graph_data(date,date,which_date)
            return JsonResponse(context)
        
        elif which_date == 'month':
            to_day = datetime.date(year,month-1,day)
            date = to_day.strftime('%m')
            context = graph_data(date,date,which_date)
            return JsonResponse(context)

        else:
            context = graph_data()
            return JsonResponse(context)
    
    return render(request, 'analysis_view.html')
