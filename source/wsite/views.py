from django.shortcuts import render, HttpResponse
from wsite.models import user_accounts
import datetime, calendar, json
from django.http import JsonResponse

# Create your views here.

# ~/
def dashboard(request):
  
  all_u = user_accounts.objects.all().count()
  act_u = user_accounts.objects.filter(_status = 1).count()
  ina_u = user_accounts.objects.filter(_status = 0).count()
  sus_u = user_accounts.objects.filter(_status = 9).count()
  
  today = datetime.datetime.now().strftime('%b %d, %Y - %A')
  c_day = int(datetime.datetime.now().strftime('%d'))
  c_month = datetime.datetime.now().month
  c_month_name = datetime.datetime.now().strftime('%B')
  c_year = datetime.datetime.now().year

  #data for line chart
  reg_eachday = []
  days_thismonth = calendar.monthrange(c_year, c_month)[1]
  day = 1;
  
  if days_thismonth == 30:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
  elif days_thismonth == 28:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
  elif days_thismonth == 29:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
  else:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]

  while day <= days_thismonth:
    reg_onthatday = user_accounts.objects.filter(_reg_at__day = day, _reg_at__month = c_month).count()
    reg_eachday.append(reg_onthatday)
    if day == c_day:
      break;
    day += 1
  
  linedata = {
    'labels' : labels,
    'datasets' : [{
      'label' : 'User Registered',
      'data' : reg_eachday,
      'borderColor' : '#3e95cd'
    }]
  }
  linedata = json.dumps(linedata)

  #data for bar chart
  reg_eachmonth = []
  reg_barcolor = []
  month = 1
  while month <= 12:
    if month <= c_month:
      reg_onthatmonth = user_accounts.objects.filter(_reg_at__month = month, _reg_at__year = c_year).count()
      reg_eachmonth.append(reg_onthatmonth)
      reg_barcolor.append('#3ecd42')
    else:
      break
    month += 1
    
    bardata = {
      'labels' : ["Jan" , "Feb" , "Mar" , "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      'datasets' : [{
        'backgroundColor' : reg_barcolor,
        'label' : 'User Registered',
        'data' : reg_eachmonth
      }]
    }
    bardata = json.dumps(bardata)
  
  #data for doughnut chart
  doughnutdata = {
    'labels' : ['Active', 'Inactive', 'Suspended'],
    'datasets' : [{
      'backgroundColor' : ["#5ee25e", "#ff4a4a", "#a9a6a6"],
      'data' : [act_u, ina_u, sus_u]
    }]
  }
  doughnutdata = json.dumps(doughnutdata)

  data = {
    'date' : today,
    'month' : c_month_name,
    'year' : c_year,
    'accounts' : {
      'all' : all_u,
      'active' : act_u,
      'inactive' : ina_u,
      'suspended' : sus_u
    },
    'charts' : {
      'line' : linedata,
      'bar' : bardata,
      'doughnut' : doughnutdata
    }
  }
  return render(request, 'dashboard.html', data)
  #return HttpResponse('this is home')
  
  
# ~/about
def about(request):
  return render(request, 'about.html')

# ~/login
def login(request):
  return render(request, 'login.html')


## Admin View Functions

#GET/POST ~/ac-admin/change-password
def adminPassUpdate(request):
  if request.method == 'GET':
    return render(request, 'admin/change_password.html')
  elif request.method == 'POST':
    return HttpResponse(request.POST.get('_password'))



## User View Functions

#GET/POST ~/accounts/new
def userCreate(request):
  if request.method == 'GET':
    return render(request, 'accounts/create.html')
  elif request.method == 'POST':
    return HttpResponse('New user data submitted')

#GET/POST ~/accounts/update/<id>
def userUpdate(request, id):
  if request.method == 'GET':
    result = user_accounts.objects.get(_id = id)
    return render(request, 'accounts/edit.html', { 'data' : result })
  elif request.method == 'POST':
    return HttpResponse('data saved')


#GET: ~/accounts/all
def usersAll(request):
  users_all = user_accounts.objects.all()
  #return HttpResponse(users_all[0]._name)
  return render(request, 'accounts/all.html', { 'users' : users_all })

#GET: ~/accounts/active
def usersAct(request):
  users_active = user_accounts.objects.filter(_status=1)
  return render(request, 'accounts/active.html', { 'users' : users_active })

#GET: ~/accounts/inactive
def usersDct(request):
  users_inactive = user_accounts.objects.filter(_status=0)
  return render(request, 'accounts/inactive.html', { 'users' : users_inactive })

#GET: ~/accounts/suspended
def usersSus(request):
  users_suspended = user_accounts.objects.filter(_status=9)
  return render(request, 'accounts/suspended.html', { 'users' : users_suspended })


#GET ~/accounts/lock/<id>
def userLock(request, id):
  if request.method == 'GET':
    return HttpResponse('edit user data')
  elif request.method == 'POST':
    return HttpResponse('data saved')
    
#GET ~/accounts/unlock/<id>
def userUnlock(request, id):
  if request.method == 'GET':
    return HttpResponse('edit user data')
  elif request.method == 'POST':
    return HttpResponse('data saved')

#GET ~/accounts/activate/<id>
def userActivate(request, id):
  if request.method == 'GET':
    return HttpResponse('edit user data')
  elif request.method == 'POST':
    return HttpResponse('data saved')

#GET ~/accounts/suspend/<id>
def userSuspend(request, id):
  if request.method == 'GET':
    return HttpResponse('edit user data')
  elif request.method == 'POST':
    return HttpResponse('data saved')
    
#POST ~/accounts/search
def userSearch(request):
  if request.method == 'GET':
    if request.is_ajax():
      if 'q' in request.GET and 's' in request.GET:
        query = request.GET.get('q')
        status = int(request.GET.get('s'))
        
        if status == 0:
          results = list(user_accounts.objects.filter(_name__icontains = query, _status = 0).values())
        elif status == 1:
          results = list(user_accounts.objects.filter(_name__icontains = query, _status = 1).values())
        elif status == 9:
          results = list(user_accounts.objects.filter(_name__icontains = query, _status = 9).values())
        else:
          results = []
      elif 'q' in request.GET:
        query = request.GET.get('q')
        results = list(user_accounts.objects.filter(_name__icontains = query).values())
      else:
        return JsonResponse({'msg': 'required parameter missing or invalid', 'data': []}, status = 400)

      return JsonResponse({'msg': 'success', 'data' : results}, status = 200)
    else:
      return JsonResponse({'msg': 'permission denied', 'data' : []}, status = 403)
  
  else:
    return JsonResponse({'msg': 'method not allowed', 'data': []}, status = 405)