#@author: Hang Liu date:13/09/17
from django.shortcuts import render
from django.http import HttpResponse
import time
from course import Course, CourseParser
from datetime import datetime, timedelta
########################################
#var
########################################

# Date & Time
#first_day = input('Enter your the first day of week 1:')
today = datetime.today()
strtoday = today.strftime("%Y%m%d")
day1_of_week1 = datetime.strptime('05/09/2016', '%d/%m/%Y')
course_id = "ULTimeTable"
course = type(Course)
subcontents = ''

########################################
#function
########################################
def index(request):
    global course_id,course
    course_id = str(request.GET['id'])
    course = Course(course_id)
    file = open(course_id+".ics","w")
    events()
    content = '''BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:'''+course_id+'''
PRODID:-//Apple Inc.//Mac OS X 10.11.4//EN
CALSCALE:GREGORIAN
X-WR-TIMEZONE:Europe/Dublin
'''+subcontents+'''
END:VCALENDAR
'''
    file.write(content)
    return HttpResponse('Course ID:'+course_id)

def week_range(wks):
    temp = wks.split(',')
    result = []
    inner = []
    for i in temp:
        a = i.split('-')
        if len(a) == 2:
            inner = [k for k in range(int(a[0]),int(a[1])+1)]
        else:
            result.append(a[0])
        for j in inner:
            result.append(j)
        inner = []
    return result

def day_event(start_time, end_time, course_id, course_type, group, teacher, class_room, weeks, event_date, week_index):
    global today
    start_time_str = datetime.strftime(datetime.strptime(start_time, '%H:%M'), '%H%M%S')
    end_time_str = datetime.strftime(datetime.strptime(end_time, '%H:%M'), '%H%M%S')
    event_date_str = event_date.strftime("%Y%m%d")
    today_str = today.strftime("%Y%m%d")
    subcontent = '''
BEGIN:VEVENT
DTSTART:'''+event_date_str+'T'+start_time_str+'''
DTEND:'''+event_date_str+'T'+end_time_str+'''
DTSTAMP:'''+event_date_str+'''T'''+start_time_str+'''
UID:-'''+event_date_str+start_time_str+end_time_str+class_room+'''
CLASS:PUBLIC
CREATED:'''+event_date_str+'''T000000Z
DESCRIPTION:'''+teacher+':'+class_room+':Wks:'+weeks+'''
LAST-MODIFIED:'''+today_str+'''T074945Z
LOCATION:Limerick
SEQUENCE:1
STATUS:CONFIRMED
SUMMARY:'''+'W'+str(week_index)+' '+class_room+' '+course_id+'-'+course_type+'-'+group+'''
TRANSP:TRANSPARENT
END:VEVENT'''
    return subcontent

#@index: which day, Mon=>0, Tue=>1, until Saturday=>5
def day_events(index):
    global subcontents,course
    courses = course.get_courses_list()
    for e in courses[index]:
        start_time = course.get_detail(e, 'START_TIME')
        end_time = course.get_detail(e, 'END_TIME')
        course_id = course.get_detail(e, 'COURSE_ID')
        course_type = course.get_detail(e, 'COURSE_TYPE')
        group = course.get_detail(e, 'GROUP')
        if group == None:
            group = ''
        teacher = course.get_detail(e, 'TEACHER')
        class_room = course.get_detail(e, 'CLASS_ROOM')
        weeks = course.get_detail(e, 'WEEKS')
        week_ranges = week_range(weeks)
        start_week_index = int(week_ranges[0]) - 1
        end_week_index = int(week_ranges[len(week_ranges)-1])
        day = day1_of_week1 + timedelta(days=index)
        for i in range(0, end_week_index):
            if i+1 in week_ranges:
                subcontents += day_event(start_time, end_time, course_id, course_type, group, teacher, class_room, weeks, day, i+1)
            day += timedelta(days=7)


def events():
    for index in range(6):
        day_events(index)

