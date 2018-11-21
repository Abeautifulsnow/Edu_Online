# -*- coding:utf-8 -*-
__author__ = 'dapeng'
__date__ = '18-10-20 上午11:17'
from django.conf.urls import url

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView,\
    TeacherListView, TeacherDeatailView

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    # 机构首页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    # 机构课程
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    # 机构介绍
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    # 机构讲师
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 讲师列表页
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),

    # 讲师详情页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDeatailView.as_view(), name='teacher_detail'),
]
