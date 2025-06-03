from django.contrib import admin
from .models import Task, PDFDocument,TaskDone, UserProfile, SubTask


admin.site.register(Task)
admin.site.register(PDFDocument)
admin.site.register(TaskDone)
admin.site.register(UserProfile)
admin.site.register(SubTask)



