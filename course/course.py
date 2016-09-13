#author: Hang Liu date:13/0917
import urllib2, urllib
import re
from HTMLParser import HTMLParser

class CourseParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = ''
        self.is_content = False
        self.col = 0
        #index1=> which day eg.: Mon, Tue, Wed
        #index2=> which course
        self.courses = [[] for i in range(6)]

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for k, v in attrs:
                if k == 'align' and v == 'justify':
                    self.is_content = True
        elif tag == 'hr' and self.is_content == True:
            self.courses[self.col].append(self.content)
            self.content = ''

    def handle_endtag(self, tag):
        if tag == 'td':
            if self.is_content == True:
                self.col += 1
                self.is_content = False

    def handle_data(self, data):
        if self.is_content and len(data.strip())>0:
            self.content += data.rstrip().lstrip()

    def reset(self):
        HTMLParser.reset(self)


class Course():
    def __init__(self, course_id):#LM039 LM634
        data = {'T1' : course_id, 'T2' : '1'}
        post = urllib2.urlopen(
            url = 'http://timetable.ul.ie/course_res.asp',
            data = urllib.urlencode(data))

        self.course_list = CourseParser()
        self.course_list.feed(post.read())

    def get_courses_list(self):
        return self.course_list.courses

    #data: eg.:12:00-13:00MA6011-LEC-MAYERHOFER EBERHARD MRSG19Wks:1-12
    def get_detail(self, data, data_type):
        pattern = re.compile(r'(\d{2}:\d{2})-(\d{2}:\d{2})([A-Z]+\d+)-([A-Z]+)-(\d+[A-Z]){0,}(.*?)((((B)|(SG)|(S)|(KBG)|(KB)|(CSG)|(CS)|(GLG)|(GL)|(FB)|(FG)|(F)|(ERB)|(ER)|(ER)|(LCB)|(LC)|(LCO)|(LB)|(LG)|(L)|(SR)|(PG)|(PM)|(P)|(HSG)|(HS)|(AM)|(A)|(BM)|(CG)|(CM)|(C)|(DG)|(DM)|(D)|(EG)|(EM)|(E)|(IWG)|(IW)){1}(M|O){0,1}\d{2,}\s{0,})+\w{0,})Wks:(.*)')        #re.compile(r'(\d{2}:\d{2})-(\d{2}:\d{2})([A-Z]+\d+)-([A-Z]+)-(\d+[A-Z]){0,}(.*?)(((B|SG|S|KBG|KB|CSG|CS|GLG|GL|FB|FG|F|ERB|ER|ER|LCB|LC|LCO|LB|LG|L|SR|PG|PM|P|HSG|HS|AM|A|BM|CG|CM|C|DG|DM|D|EG|EM|E|IWG|IW|M|O)+\d+\s{0,})+\w{0,})Wks:(.*)')
        match = pattern.match(data)
        if match:
            if data_type == 'START_TIME':
                return match.group(1)
            elif data_type == 'END_TIME':
                return match.group(2)
            elif data_type == 'COURSE_ID':
                return match.group(3)
            elif data_type == 'COURSE_TYPE':
                return match.group(4)
            elif data_type == 'GROUP':
                return match.group(5)
            elif data_type == 'TEACHER':
                return match.group(6)
            elif data_type == 'CLASS_ROOM':
                return match.group(7)
            elif data_type == 'WEEKS':
                return match.group(52)
            else:
                return

#CourseParser.get_time(course_list.courses[2][2])
#CourseParser.get_module_id(course_list.courses[2][2])
#print CourseParser.get_detail(course_list.courses[2][1],'END_WEEK')



