"""Edu_online path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path('', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.paths import include, path
    2. Add a path to pathpatterns:  path('blog/', include('blog.paths'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static

import xadmin
from Edu_online.settings import MEDIA_ROOT, MEDIA_URL

from users.views import LoginView, RegisterView, LogoutView, ModifyPwdView, ResetView, ActiveUserView, ForgetPwdView, \
    IndexView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin', xadmin.site.urls),
    # 网站主页
    path('', IndexView.as_view(), name="index"),
    # 登录界面
    path('login/', LoginView.as_view(), name='login'),
    # 用户退出登录
    path('logout/', LogoutView.as_view(), name='logout'),
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    # 验证码图片路径
    path('captcha/', include('captcha.urls')),
    # 注册激活
    re_path(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    # 找回密码
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    # 密码重置
    re_path(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    # 密码修改
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    # captcha
    path('captcha/', include("captcha.urls")),
    # app path dispatch
    path('org/', include('organization.urls', namespace='org')),
    path('course/', include('courses.urls', namespace='course')),
    path('users/', include('users.urls', namespace='users')),

    # 富文本编辑器
    path('ueditor/', include('DjangoUeditor.urls')),
]

# media上传配置
# urlpatterns += [re_path(r'^media/(?P<path>.*)/$', serve, {"document": MEDIA_ROOT}),]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
# Debug=False时，配置静态资源
# urlpatterns += static(STATIC_path, document_root=STATIC_ROOT)


# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.server_error'
# 全局403页面配置
handler403 = 'users.views.permission_denied'
