from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from personal.views import (
		home_screen_view,
)
from account.views import (
		register_view,
	)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name = "home"),
    path('register/', register_view, name = "register"),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)