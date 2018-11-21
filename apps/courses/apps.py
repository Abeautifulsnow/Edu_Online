# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

# 设置app的相关配置,比如下面使用的中文名字
class CoursesConfig(AppConfig):
    name = 'courses'
    verbose_name = '课程管理'