from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import index, JummahKhateebView

urlpatterns = [
    path('', index, name='Index'),
    path('jummah/v1/jummah_khateeb/', JummahKhateebView.as_view(), name='Jummah Khateeb'),
    path('jummah/v1/jummah_khateeb/<date>/', JummahKhateebView.as_view(), name='Jummah Khateeb'),
]

urlpatterns = format_suffix_patterns(urlpatterns)