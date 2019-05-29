import datetime
from django.http import HttpResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .serializers import JummahKhateebSerializer, SalaahTimeSerializer

from .jummah_khateeb import khateeb_finder
from .converters_formatter import string2datetime, create_pandas_query
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


class SalaahTimesView(views.APIView):
    """Returns a list of Salaah time for a given date(s)"""

    def get(self, request, *args, **kwargs):
        yyyy = int(kwargs.get('year')) if kwargs.get('year') else kwargs.get('year')
        mm = int(kwargs.get('month')) if kwargs.get('month') else kwargs.get('month')
        dd = int(kwargs.get('day')) if kwargs.get('day') else kwargs.get('day')

        query = create_pandas_query(year=yyyy, month=mm, day=dd)

        non_serial = {'date': '{}'.format(query)}

        data = SalaahTimeSerializer(non_serial).data

        return Response(data)

