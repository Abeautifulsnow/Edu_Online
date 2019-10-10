import os
import sys
import django

from db_tools.data.course import row_data
from courses.models import Lesson, Course

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pwd + '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Edu_online.settings')


django.setup()


for lesson_details in row_data:
    lesson = Lesson()
    course_name = lesson_details['course'][0]
    course = Course.objects.filter(name=course_name)
    if course:
        lesson.course = course[0]
    lesson.name = lesson_details['name']
    lesson.learn_times = lesson_details['learn_times']
    lesson.save()
