from django.urls import path
from .views import *

app_name = 'chart'

urlpatterns = [
    path('', summary_chart, name='summary_chart'),
    path('word_population/', world_population, name='world_population'),  # !!!
    path('ticket_class_1/', ticket_class_view_1, name='ticket_class_view_1'),
    path('ticket_class_2/', ticket_class_view_2, name='ticket_class_view_2'),
    path('ticket_class_3/', ticket_class_view_3, name='ticket_class_view_3'),
    path('json_example/', json_example, name='json_example'),
    path('json-example/data/', chart_data, name='chart_data'),
    path('covid_19/', covid_19_view, name='covid_19_view'),
]
