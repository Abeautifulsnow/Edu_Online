import xadmin

from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-building-o'
    relfield_style = 'fk-ajax'

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'tag', 'category', 'click_nums', 'fav_nums', 'image', 'address', 'city',  'students', 'course_nums', 'add_time']
    search_fields = ['name', 'desc', 'tag', 'category', 'click_nums', 'fav_nums', 'image', 'address', 'city__name']
    list_filter = ['name', 'desc', 'tag', 'category', 'click_nums', 'fav_nums', 'image', 'address', 'city',  'students', 'course_nums', 'add_time']
    model_icon = 'fa fa-institution (alias)'
    # 将外键设置为异步搜索模式
    relfield_style = 'fk-ajax'

class TeacherAdmin(object):
    list_display = ['org', 'name', 'age', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org__name', 'name', 'age', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    model_icon = 'fa fa-drivers-license (alias)'
    relfield_style = 'fk-ajax'

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
