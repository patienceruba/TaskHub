from django.contrib import admin
from .models import RecordRow, PDFDocument,TaskDone, UserProfile, SubTask


admin.site.register(RecordRow)
admin.site.register(PDFDocument)
admin.site.register(TaskDone)
admin.site.register(UserProfile)
admin.site.register(SubTask)


