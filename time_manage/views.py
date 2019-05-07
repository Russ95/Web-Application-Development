from django.shortcuts import render
from django.db.models import Q
import os
# Create your views here.

# Create your views here.

# from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from time_manage.forms import LoginForm, RegistrationForm, CreateForm, EditForm
from django.http import StreamingHttpResponse
from datetime import datetime, timedelta, date
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from .models import *
from .utils import Calendar
from .forms import EventForm

from django.core import serializers
import json
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *
# from .utils import Calendar
# from .forms import EventForm


def getuser(request):
    return request.user

@login_required
def home_page(request):
    current_day = datetime.now().date()   #2019-04-16
    print (current_day)
    all_items = Event.objects.filter(user=request.user,is_finished=False)
    # all_items = Event.objects.filter(user=request.user)
    for item in all_items:
        print (item.start_time)
    print ('all_items:::',all_items)
    context={}
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
    context['date']=year+'_'+month+'_'+str(day)
    context['user']=request.user
    context['items']=all_items

    # return render(request, 'time_manage/main_page.html', context)
    return render(request, 'time_manage/index.html', context)

@login_required
def mark_as_finished(request,item_id):   #mark both!!!
    print (item_id)
    post = Event.objects.get(id=item_id)
    if post.is_finished==False:
        post.is_finished = True
    else:
        post.is_finished = False
    post.save()

    current_day = datetime.now().date()   #2019-04-16
    print (current_day)
    all_items = Event.objects.filter(user=request.user,is_finished=False)
    # all_items = Event.objects.filter(user=request.user)
    for item in all_items:
        print (item.start_time)
    print ('all_items:::',all_items)
    context={}
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
    context['date']=year+'_'+month+'_'+str(day)
    context['user']=request.user
    context['items']=all_items

    # return render(request, 'time_manage/main_page.html', context)
    return render(request, 'time_manage/index.html', context)

@login_required
def finished_event(request):
    event=Event.objects.filter(user=request.user,is_finished=True)
    context={}
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
    context['date']=year+'_'+month+'_'+str(day)
    context['user']=request.user
    context['items']=event

    # return render(request, 'time_manage/main_page.html', context)
    return render(request, 'time_manage/finished_event.html', context)

@login_required
def current_day(request):
    current_day = datetime.now().date()   #2019-04-16
    print (current_day)
    all_items = Event.objects.filter(user=request.user,start_time__contains=current_day)
    print ('current_items:::',all_items)

    context={}
    context['msg']=request.user
    context['items']=all_items
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
    context['date']=year+'_'+month+'_'+str(day)

    # return render(request, 'time_manage/main_page.html', context)
    return render(request, 'time_manage/current_day.html', context)

@login_required
def history(request,date=None):
    print (date)
    year,month,day=date.split('_')
    if len(month)==1:
        month='0'+month
    if len(day)==1:
        day='0'+day
    that_day=year+'-'+month+'-'+day
    # current_day = datetime.now().date()   #2019-04-16
    print (that_day)
    all_items = Event.objects.filter(user=request.user,start_time__contains=that_day)
    print ('current_items:::',all_items)
    # print (item)

    # try:
    #     newuser=Profile.objects.get(user=request.user)
    # except:
    #     newuser=Profile(user=request.user)
    #     newuser.save()
    context={}
    context['msg']=request.user
    context['items']=all_items
    context['date']=that_day
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
    context['date_']=year+'_'+month+'_'+str(day)

    # return render(request, 'time_manage/main_page.html', context)
    return render(request, 'time_manage/history.html', context)


def index(request):
    return HttpResponse('<p>index page</p>')

class CalendarView(generic.ListView):
    # global user_forclass
    # model = Event.objects.filter(user=CalendarView.get())
    # print ('basic here')
    model = Event

    # uu=get(request)

    print ('model:::',model)
    template_name = 'time_manage/calendar_test.html'
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(CalendarView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        print ('previous context',context)
        context.update({
        'object_list': Event.objects.filter(user=self.request.user),
        'event_list': Event.objects.filter(user=self.request.user)
    })    #useful but not affect followings
        print ('mid-context',context)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month,self.request.user)  #it is here so we should pass request.user to utils
        # context.fields['user'].queryset = Event.objects.filter(user=self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        # context['user']=request.user
        current_day = datetime.now().date()   #2019-04-16
        year,month,day=str(current_day).split('-')
        day=str(int(day)-1)
        if len(day)==1:
            day='0'+str(day)
        context['date']=year+'_'+month+'_'+str(day)
        print ('will it be here')
        print ('context',context)
        return context
    # def get_form(self, model=None):
    #     form = super().get_form(model)
    #     form = Event.objects.filter(user=self.request.user)
    #     return form

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
@login_required
def event(request, event_id=None):
    print ('eventid:::',event_id)
    user=request.user
    instance = Event(user=user)
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event(user=user)
    print (instance)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        # return HttpResponseRedirect(reverse('cal:calendar'))
        return HttpResponseRedirect(reverse('time_manage:calendar'))
        # return redirect(reverse('calendar'))
    # return render(request, 'time_manage/event_test_2.html', {'form': form,'event_id':event_id})
    return render(request, 'time_manage/event_test_2.html', {'form': form,'event_id':event_id})


def delete_event(request, event_id=None):
    user=request.user
    Event.objects.filter(id=event_id).delete()
    print ('success')
    return HttpResponseRedirect(reverse('time_manage:calendar'))
@login_required
def classifier(request):   #just display
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
    
    print ('classifier')
    
    total_monitored=Item.objects.filter(username=request.user,type='Unknown').values('process_name','type').distinct()
    # known_monitored=Item.objects.filter(username=request.user).exclude(type='Unknown').values('process_name').distinct()
    known_monitored=Item.objects.filter(username=request.user).exclude(type='Unknown').values('process_name','type').distinct()
    print ('total_monitored',total_monitored)
    print ('known',known_monitored)
    total_monitored=total_monitored | known_monitored
    print ('total_monitored',total_monitored)
    context={}
    context['date']=year+'_'+month+'_'+str(day)
    context['user']=request.user
    context['items']=total_monitored[::-1]
    return render(request, 'time_manage/classifier.html',context)

@login_required
def category(request,item_name,item_category):  #make category
    total_monitored=Item.objects.filter(username=request.user).values('process_name').distinct()
    print ('total_monitored',total_monitored)
    print ('category:::',item_name,item_category)
    # return render(request, 'time_manage/classifier.html',context)
    current_item=Item.objects.filter(username=request.user,process_name=item_name)
    for each in current_item:
        each.type=item_category
        each.save()
    # current_item.type=item_category
    # current_item.save()
    message='hello'
    # return render(request, 'time_manage/classifier.html',context)
    return redirect(reverse('time_manage:classifier'))

@login_required
def effect_rank(request):
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
        
    total_event=Item.objects.filter(username=request.user)
    print ('total_event',total_event)
    effect_dic={'Software_Development':5,'Reference':4,'Entertainment':-3,'Social':1,'Unknown':0}
    effect_point=[5,4,-3,1,0]
    # all_user=Item.objects.filter(username=request.user).values('username').distinct()
    all_user=Item.objects.all().values('username').distinct()
    print ('all_user:::',all_user)
    final_dic={}
    for item in all_user:
        uname=item['username']   #russ958
        print ('uname',uname)
        software=Item.objects.filter(username=uname,type='Software_Development')
        reference=Item.objects.filter(username=uname,type='Reference')
        entertainment=Item.objects.filter(username=uname,type='Entertainment')
        social=Item.objects.filter(username=uname,type='Social')
        unknown=Item.objects.filter(username=uname,type='Unknown')
        print ('software',software)
        print ('reference',reference)
        print ('entertainment',entertainment)
        print ('social',social)
        print ('Unknown',unknown)
        time_allocate={}
        software_time=0
        for item in software.iterator():
            # print (item)
            time_gap=item.update_time-item.create_time
            # print (time_gap)
            hour,minute,second=str(time_gap).split(':')
            second=second.split('.')[0]
            software_time+=int(hour)*60+int(minute)+int(second)/60
        print ('software_time',software_time)
        time_allocate['software_time']=software_time

        reference_time=0
        for item in reference.iterator():
            # print (item)
            time_gap=item.update_time-item.create_time
            # print (time_gap)
            hour,minute,second=str(time_gap).split(':')
            second=second.split('.')[0]
            reference_time+=int(hour)*60+int(minute)+int(second)/60
        print (reference_time)
        time_allocate['reference_time']=reference_time

        entertainment_time=0
        for item in entertainment.iterator():
            # print (item)
            time_gap=item.update_time-item.create_time
            # print (time_gap)
            hour,minute,second=str(time_gap).split(':')
            second=second.split('.')[0]
            entertainment_time+=int(hour)*60+int(minute)+int(second)/60
        print (entertainment_time)
        time_allocate['entertainment_time']=entertainment_time
        
        social_time=0
        for item in social.iterator():
            # print (item)
            time_gap=item.update_time-item.create_time
            # print (time_gap)
            hour,minute,second=str(time_gap).split(':')
            second=second.split('.')[0]
            social_time+=int(hour)*60+int(minute)+int(second)/60
        print (social_time)
        time_allocate['social_time']=social_time


        unknown_time=0
        for item in unknown.iterator():
            # print (item)
            time_gap=item.update_time-item.create_time
            # print (time_gap)
            hour,minute,second=str(time_gap).split(':')
            second=second.split('.')[0]
            unknown_time+=int(hour)*60+int(minute)+int(second)/60
        print (unknown_time)
        time_allocate['unknown_time']=unknown_time

        print ('time_allocate:::',time_allocate)
        #{'software_time': 45.18333333333333, 
        # 'reference_time': 14.899999999999997, 'entertainment_time': 0, 
        # 'social_time': 0.0, 'unknown_time': 3.333333333333333}
        final_point_this_user=time_allocate['software_time']*effect_point[0]+time_allocate['reference_time']*effect_point[1] \
                    +time_allocate['entertainment_time']*effect_point[2]+time_allocate['social_time']*effect_point[3] \
                    +time_allocate['unknown_time']*effect_point[4]
        final_dic[uname]=final_point_this_user

    print (final_dic)
    points=list(final_dic.values())
    print (points)
    points.sort(reverse=True)
    final_param=[]
    rank=1
    for item in points:
        tmp=[]
        tmp.append(rank)
        tmp.append(list(final_dic.keys())[list(final_dic.values()).index(item)])
        tmp.append(item)
        rank+=1
        final_param.append(tmp)
    context={}
    # context['items']=[[1,'russ958',370],[2,'ziyug',260]]
    context['items']=final_param
    context['date']=year+'_'+month+'_'+str(day)
    return render(request, 'time_manage/effect_list_test.html',context)



@login_required
def about(request):
    context={}
    context['msg']=request.user
    current_day = datetime.now().date()   #2019-04-16
    year,month,day=str(current_day).split('-')
    day=str(int(day)-1)
    if len(day)==1:
        day='0'+str(day)
    context['date']=year+'_'+month+'_'+str(day)
    return render(request, 'time_manage/about.html',context)


def file_download(request):
    file=open('/home/ubuntu/team29/time_manage/static/main.py','r')
    filedata=file.read()

    filedata=filedata.replace('123',str(request.user))
    with open('/home/ubuntu/team29/time_manage/static/your_monitor.py','w') as file_:
        file_.write(filedata)
    file_2=open('/home/ubuntu/team29/time_manage/static/your_monitor.py','rb')
    response =HttpResponse(file_2)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="your_monitor.py"'

    return response

#三件套
def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'time_manage/login_test.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'time_manage/login_test.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('time_manage:home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('time_manage:login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        # print (context)
        return render(request, 'time_manage/register_test.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'time_manage/register_test.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        # email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('time_manage:home'))


def historyrecord(request):
    return render(request, 'monitor/action_record.html', {})


def add_item(request):
    if request.method != 'POST':
        raise Http404

    if not 'item' in request.POST or not request.POST['item']:
        message = 'You must enter an item to add.'
        json_error = '{ "error": "' + message + '" }'
        return HttpResponse(json_error, content_type='application/json')

    jsondata = json.loads(request.POST['item'])
    # print(type(jsondata['create_time']))
    try:
        last_item = Item.objects.filter(username = jsondata['username']).latest('id')
    except:
        last_item = None

    try:
        type_name = Item.objects.filter(username = jsondata['username'],process_name=jsondata['process_name']).earliest('id').type
        print ('type_name:::',type_name)
    except:
        print ('new addition to here')
        type_name = 'Unknown'

    if last_item is not None and jsondata['process_name'] == last_item.process_name:
        print(1)
        last_item.update_time = jsondata['update_time']
        last_item.save()
    # elif last_item is not None:
    elif last_item is None:
        #print(2);
        new_item = Item(process_name=jsondata['process_name'],
                        ip_addr=request.META['REMOTE_ADDR'],
                        update_time=jsondata['update_time'],
                        create_time=jsondata['update_time'],
                        # type=type_name,
                        type='Unknown',
                        username=jsondata['username'])
        new_item.save()
    else:
        print(3)
        new_item = Item(process_name=jsondata['process_name'],
                        ip_addr=request.META['REMOTE_ADDR'],
                        update_time=jsondata['update_time'],
                        create_time=last_item.update_time,
                        # type='Unknown',
                        type=type_name,
                        username=jsondata['username'])
        new_item.save()

    response_text = serializers.serialize('json', Item.objects.all())
    return HttpResponse(response_text, content_type='application/json')


def delete_item(request, item_id):
    if request.method != 'POST':
        raise Http404

    item = get_object_or_404(Item, id=item_id)
    item.delete()

    response_text = serializers.serialize('json', Item.objects.all())
    return HttpResponse(response_text, content_type='application/json')


def get_list_json(request):
    response_text = serializers.serialize('json', Item.objects.all())
    return HttpResponse(response_text, content_type='application/json')

@login_required
def get_graph(request):
    return render(request, 'monitor/graph.html', {})

@login_required
def get_my_list_json(request):
    response_text = serializers.serialize('json', Item.objects.filter(username = request.user))
    return HttpResponse(response_text, content_type='application/json')

@login_required
def get_history_date(request, date_str):
    time = date_str.split("_")

    response_text = serializers.serialize('json', Item.objects.filter(username = request.user, update_time__year = time[0], update_time__month = time[1], update_time__day = time[2]))
    return HttpResponse(response_text, content_type='application/json')


@login_required
def get_future_event(request):
    current_day = datetime.now().date()
    year,month,day=str(current_day).split('-')
    print (current_day)
    print (day)
    response_text = serializers.serialize('json', Event.objects.filter(user = request.user, start_time__year = year, start_time__month = month, start_time__day__gte = day))
    return HttpResponse(response_text, content_type='application/json')

@login_required
def get_plan_day(request, date_str):
    time = date_str.split("_")

    response_text = serializers.serialize('json', Event.objects.filter(user = request.user, start_time__year = time[0], start_time__month = time[1], start_time__day = time[2]))
    return HttpResponse(response_text, content_type='application/json')
