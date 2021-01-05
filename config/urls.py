from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500, handler400

handler404 = 'recipes.views.page_not_found'
handler500 = 'recipes.views.server_error'
handler400 = 'recipes.views.page_bad_request'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('', include('recipes.urls')),
]


# urlpatterns += [
#     path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
#     path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
# ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
