# -*- coding:utf-8 -*-
__author__ = 'dapeng'
__date__ = '18-10-23 上午9:39'

from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentView, AddCommentView, VideoPlay

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程视频信息
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_video'),
    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    # 添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    # 视频播放
    url(r'^video/(?P<video_id>\d+)/$', VideoPlay.as_view(), name='video_play'),
]
