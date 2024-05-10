from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from main.views import error_404,error_500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")) # This line tells Django to include the urls.py file from the main app
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# handler404 = error_404
# handler500 = error_500
