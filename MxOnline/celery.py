# -*- coding:utf-8 -*-
from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# 获取项目名称
proj_name = os.path.split(os.path.abspath('.'))[-1]
proj_settings = '%s.settings' % proj_name

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', proj_settings)

# 实例化celery
app = Celery(proj_name)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'