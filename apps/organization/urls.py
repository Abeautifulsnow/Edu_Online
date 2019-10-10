from django.urls import path

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView,\
    TeacherListView, TeacherDeatailView


app_name = 'organization'

urlpatterns = [
    # 课程机构列表页
    path('list/', OrgView.as_view(), name="org_list"),
    path('add_task/', AddUserAskView.as_view(), name="add_ask"),
    # 机构首页
    path('home/<int:org_id>/', OrgHomeView.as_view(), name="org_home"),
    # 机构课程
    path('course/<int:org_id>/', OrgCourseView.as_view(), name="org_course"),
    # 机构介绍
    path('desc/<int:org_id>/', OrgDescView.as_view(), name="org_desc"),
    # 机构讲师
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
    # 讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 讲师详情页
    path('teacher/detail/<int:teacher_id>/', TeacherDeatailView.as_view(), name="teacher_detail"),
]
