"""
This will make sure the app is always imported when
Django starts so that shared_task will use this app.
you need to import this app in your proj/proj/__init__.py
module. This ensures that the app is loaded when Django
starts so that the @shared_task decorator (mentioned later)
will use it
"""

from drf_course.celery import app as celery_app

__all__ = ("celery_app",)
