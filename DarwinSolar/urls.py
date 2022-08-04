from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ds/', include('ds.api.urls')),
    path('api/accounts/', include('accounts.api.urls')),
    path('api/customer/', include('customer_portal.api.urls')),
    path('api/app/', include('company.api.app.urls')),
    path('api/company/', include('company.api.company_api.urls')),
    path('api/installer/', include('company.api.installer_api.urls')),


    path('stats/', include('stats.urls')),
    # path('', TemplateView.as_view(template_name='index.html')),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

