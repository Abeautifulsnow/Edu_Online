# encoding:utf-8
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView
from users.views import IndexView
from MxOnline.settings import MEDIA_ROOT   # STATIC_ROOT

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # xadmin后台管理路由
    url(r'xadmin/', xadmin.site.urls),
    # 网站主页
    url(r'^$', IndexView.as_view(), name='index'),
    # 登录界面
    url(r'^login/$', LoginView.as_view(), name='login'),
    # 用户退出登录
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 注册
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 验证码图片路径
    url(r'^captcha/', include('captcha.urls')),
    # 注册激活
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    # 找回密码
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    # 密码重置
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    # 密码修改
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构URL配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程相关URL配置
    url(r'^course/', include('courses.urls', namespace='course')),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # 用户相关URL配置
    url(r'^users/', include('users.urls', namespace='users')),

    # debug=False环境下静态资源
    url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),

    # 富文本编辑器url
    url(r'^ueditor/', include('DjangoUeditor.urls'))
]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.server_error'
# 全局403页面配置
handler403 = 'users.views.permission_denied'
