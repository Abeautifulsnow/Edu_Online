# -*- coding:utf-8 -*-
__author__ = 'dapeng'
__date__ = '18-10-30 上午10:28'

from django.conf.urls import url

from .views import UserInfoView, ImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, UserMessageView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 用户图像上传
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 邮箱验证码发送
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # 我收藏的授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 我收藏的公开课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    # 我的消息
    url(r'^message/$', UserMessageView.as_view(), name='message'),

]