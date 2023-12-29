from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('athletes.urls')),
    path('', include('users.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

admin.site.site_header = 'Администрирование'
admin.site.index_title = 'Мировые спортсмены'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
