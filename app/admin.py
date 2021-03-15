from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.class_room)
admin.site.register(models.department)
admin.site.register(models.user_profile)
admin.site.register(models.course)
admin.site.register(models.session)
admin.site.register(models.course_enrolled)
admin.site.register(models.attendance)
