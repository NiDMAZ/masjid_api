from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import index, JummahKhateebView, SalaahTimesView


urlpatterns = [
    path('', index, name='Index'),
    path('jummah/v1/jummah_khateeb/', JummahKhateebView.as_view(), name='Jummah Khateeb'),
    path('jummah/v1/jummah_khateeb/<date>/', JummahKhateebView.as_view(), name='Jummah Khateeb'),
    re_path(r'salaah/v1/salaah/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})?/?(?P<day>[0-9]{1,2})?', SalaahTimesView.as_view(), name='Salaah Times')
]

urlpatterns = format_suffix_patterns(urlpatterns)