import datetime
from django.http import HttpResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .serializers import JummahKhateebSerializer

from .jummah_khateeb import khateeb_finder
from .converters_formatter import string2datetime
# Create your views here.


def index(request):
    return HttpResponse("Hello World!, you have reached the index")


class JummahKhateebView(views.APIView):
    """Returns the Jummah Khateeb for a given date"""

    def get(self, request, *args, **kwargs):
        request_date = string2datetime(str(kwargs.get('date', datetime.datetime.now())))

        non_serial = khateeb_finder.get_khateeb_for_date(request_date)

        if non_serial is not None:
            data = JummahKhateebSerializer(non_serial).data
            return Response(data)
        else:
            content = {'error': 'No Khateeb information for date: {}, try another date'.format(request_date)}
            return Response(content, status.HTTP_404_NOT_FOUND)
