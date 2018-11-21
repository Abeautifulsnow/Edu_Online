# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

class CourseListView(View):
    """
    课程列表详情页
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        # 热门推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|
                                             Q(detail__icontains=search_keywords))

        # 最热门或参与人数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'new':
                all_courses = all_courses.order_by('-add_time')

        # 课程列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 5, request=request)
        courses = p.page(page)

        context = {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        }
        return render(request, 'course-list.html', context)


class VideoPlay(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 筛选出用户的课程
        user_courses = UserCourse.objects.filter(course=course)
        # 取出用户的所有id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出该用户id的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('click_nums')[:5]

        # 课程资源
        all_resources = CourseResource.objects.filter(course=course)

        context = {
            'course': course,
            'course_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video
        }
        return render(request, 'course-play.html', context)


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_favor_course = False
        has_favor_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_favor_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_favor_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        context = {
            'course': course,
            'relate_courses': relate_courses,
            'has_favor_course': has_favor_course,
            'has_favor_org': has_favor_org
        }
        return render(request, 'course-detail.html', context)


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 筛选出用户的课程
        user_courses = UserCourse.objects.filter(course=course)
        # 取出用户的所有id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出该用户id的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('click_nums')[:5]

        # 课程资源
        all_resources = CourseResource.objects.filter(course=course)

        context = {
            'course': course,
            'course_resources': all_resources,
            'relate_courses': relate_courses
        }
        return render(request, 'course-video.html', context)


class CommentView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 筛选出用户的课程
        user_courses = UserCourse.objects.filter(course=course)
        # 取出用户的所有id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出该用户id的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        # 按照评论时间倒叙排列
        all_comments = CourseComments.objects.filter(course=course).order_by('-add_time')

        context = {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses

        }
        return render(request, 'course-comment.html', context)


class AddCommentView(View):
    """
    用户发表评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', "")
        if course_id > 0 and comments:
            # 实例化CourseComments
            course_comments = CourseComments()
            course = Course.objects.get(id=course_id)
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            # 固定写法
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')
