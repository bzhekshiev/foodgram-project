from django.conf import settings
from django.conf.urls import handler400, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = 'config.views.page_not_found'  # noqa
handler500 = 'config.views.server_error'  # noqa
handler400 = 'config.views.page_bad_request'  # noqa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('', include('recipes.urls')),
]


urlpatterns += [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('tech/', views.flatpage, {'url': '/tech/'}, name='tech'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
