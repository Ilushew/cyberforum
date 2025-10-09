from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('courses/', include('courses.urls')),
    path('search/', include('search.urls')),
    path('news/', include('news.urls')),
    path('events/', include('events.urls')),
    path('documentation/', include('documentation.urls')),
    path('moderator/', include('moderation.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)