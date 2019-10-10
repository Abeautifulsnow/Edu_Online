# celery异步发送邮件步骤

## 步骤

* settings.py根目录下创建---> celery.py
* 在根目录__init__.py中写入：
```python
from __future__ import absolute_import, unicode_literals

from Edu_online.celery import app as celery_app

# 给外部模块提供访问接口
__all__ = ['celery_app']
```
* settings.py中编写celery的配置项
* app下创建需要使用celery的文件**tasks.py**，并在对应函数中使用(delay)
* 在manage.py这一级目录下运行celery:
```bash
celery -A Edu_online worker -l info

```
