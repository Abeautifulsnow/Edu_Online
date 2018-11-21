# encoding:utf-8
import json
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from pure_pagination import PageNotAnInteger, Paginator

from users.models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    """
    邮箱激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对密码明文加密
            user_profile.password = make_password(pass_word)
            # 保存
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})

class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        return render(request, 'login.html', {})
    
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():   # 验证
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ForgetPwdView(View):
    """
    忘记密码
    """
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    """
    密码重置
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')  # 对应于html文件中input属性中name
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, "modify_form": ''})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, requset):

        context = {

        }
        return render(requset, 'usercenter-info.html', context)

    def post(self, request):
        user_info_form = UserInfoForm(data=request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()

            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class ImageUploadView(LoginRequiredMixin, View):
    """
    用户图像上传
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    用户个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')  # 对应于html文件中input属性中name
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已经注册"}', content_type='application/json')
        send_register_email(email, 'update_email')

        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        exited_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if exited_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)

        context = {
            'user_courses': user_courses
        }
        return render(request, 'usercenter-mycourse.html', context)


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我的收藏:机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        context = {
            'org_list': org_list,
        }

        return render(request, 'usercenter-fav-org.html', context)


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我的收藏:教师
    """
    def get(self, request):
        # 创建空列表
        teacher_list = []
        # 从UserFavorite中取出来教师这个收藏类型
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        context = {
            'teacher_list': teacher_list,
        }

        return render(request, 'usercenter-fav-teacher.html', context)


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我的收藏:公开课程
    """
    def get(self, request):
        # 创建空列表
        course_list = []
        # 从UserFavorite中取出来课程这个收藏类型
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        context = {
            'course_list': course_list,
        }

        return render(request, 'usercenter-fav-course.html', context)


class UserMessageView(LoginRequiredMixin, View):
    """
    用户消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)

        context = {
            'messages': messages
        }
        return render(request, 'usercenter-message.html', context)


class IndexView(View):
    """
    慕学在线网首页
    """

    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 不是轮播图的课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 是轮播图的课程
        banner_courses = Course.objects.filter(is_banner=True)[:2]
        # 课程机构
        course_orgs = CourseOrg.objects.all()[:15]

        context = {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        }
        return render(request, 'index.html', context)


def page_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def server_error(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

def permission_denied(request):
    # 全局403处理函数
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response
