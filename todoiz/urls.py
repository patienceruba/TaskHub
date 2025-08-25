from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('api/', include('notifications.urls')),
    path('userau', include('userAuthent.urls')),
    path('team', include('teams.urls')),
    path('chat', include('chat.urls')),
    path("assigntask", include("assigntask.urls")),
    path("editProfile", include("profile_edit.urls")),
    path('sileProfile', include("slide_profile.urls")),
    path('files', include("files.urls"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)