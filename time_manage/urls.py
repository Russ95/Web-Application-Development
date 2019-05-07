from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url
app_name = 'time_manage'   #影响登陆
urlpatterns = [
    path('', views.home_page, name='home'),
    path('current_day', views.current_day, name='current_day'),
    path('finished_event',views.finished_event,name='finished_event'),
    path('about', views.about, name='about'),
    path('download', views.file_download, name='download'),
    path('history/<str:date>', views.history, name='history'),
    path('classifier', views.classifier, name='classifier'),
    path('efficiency', views.effect_rank, name='efficiency'),
    path('category/<str:item_name>/<str:item_category>', views.category, name='category'),
    # 'photo/<int:id>'
    # url(r'^history/(?P<date>\d+)/$', views.history, name='history'),
    path('calendar',views.CalendarView.as_view(), name='calendar'),
    path('marked/<int:item_id>',views.mark_as_finished, name='marked'),
    url(r'^index/$', views.index, name='index'),
    url(r'^event/new/$', views.event, name='event_new'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    url(r'^event/delete/(?P<event_id>\d+)/$', views.delete_event, name='delete'),
    # path('',views.delete_event,name='delete'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),

    path('historyrecord', views.historyrecord),
    path('add-item', views.add_item),
    path('delete-item/<int:item_id>', views.delete_item),
    path('get-list-json', views.get_list_json),
    path('get-my-list-json', views.get_my_list_json),
    path('get-history-date/<str:date_str>', views.get_history_date),
    path('graph', views.get_graph),

    path('future_event', views.get_future_event),
    path('plan_event/<str:date_str>', views.get_plan_day)
]