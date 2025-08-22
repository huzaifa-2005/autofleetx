from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('accounts/', include('allauth.urls')),
    path("api/", include("api.urls")),
]

# Media files handling - FIXED VERSION
if settings.DEBUG:
    # Development: serve both static and media files locally
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
# NO else clause needed for production!
# Cloudinary handles media files automatically, no URL routing needed