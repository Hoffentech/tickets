from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url('admin/', admin.site.urls),
    url('', include('core.urls')),     
    url('backoffice/', include('backoffice.urls')),     

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'tickets Manager'
admin.site.site_title = 'tickets Manager'