from __future__ import absolute_import, unicode_literals


import os
from celery import Celery
from django.conf import settings


# 获取项目名称,split()分割最后一个'/'前后并保留'/'之后的部分,abspath()提取绝对路径
proj_name = os.path.split(os.path.abspath('.'))[-1]
proj_settings = '%s.settings' % proj_name

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', proj_settings)

# 实例化celery
app = Celery(proj_name)
# 读取配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
