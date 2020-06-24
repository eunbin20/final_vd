# hChart.urls.py
from django.contrib import admin

from django.urls import path
from chart import views
from django.urls import path, include # !!!
from django.contrib.auth import urls
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [
    # path('', views.home, name='home'),

      # !!!
    # path('json-example/', views.json_example, name='json_example'),
    # path('json-example/data/', views.chart_data, name='chart_data'),
    path('admin/', admin.site.urls),
    path('', include('chart.urls')),
    path('accounts/', include('accounts.urls')),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

