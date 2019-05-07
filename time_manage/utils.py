from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from .views import *

#https://docs.python.org/3/library/calendar.html
#info for HTMLCalendar
# gogo=getuser()
class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None,user=None):
		self.year = year
		self.month = month
		self.user=user
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		# print ('events_per_day:::',events_per_day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'

		if day != 0:
			# return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
			tmp="<td><span class='date'>"
			tmp+="<a href='/time_manage/history/{}'>".format(str(self.year)+'_'+str(self.month)+'_'+str(day))
			
			tmp+="{}".format(day)
			tmp+="</a></span><ul> {} </ul></td>".format(d)
			return tmp

			# return f"<td><span class='date'><a href='{% url 'time_manage:delete' event_id %}'>{day}</a></span><ul> {d} </ul></td>"
			# return "<td><span class='date'><a href='{}'>{day}</a></span><ul> {d} </ul></td>".format("'%' url 'time_manage:delete' event_id %")
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month,user=self.user)
		print ('event',events)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal
