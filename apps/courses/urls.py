from django.urls import path, re_path
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentView, VideoPlay, AddCommentView

app_name = "courses"

urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name='course_list'),
    # 课程详情
    re_path(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程视频信息
    re_path(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_video'),
    # 课程评论
    re_path(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    # 添加课程评论
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    # 视频播放
    re_path(r'^video/(?P<video_id>\d+)/$', VideoPlay.as_view(), name='video_play'),
]
