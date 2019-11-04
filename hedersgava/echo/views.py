from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response as response
from echo.parsers import XMLParser
from rest_framework.parsers import BaseParser
import datetime
from echo.models import Device,Element
from echo.serializers import ElementSerializer
import xml.etree.cElementTree as ET
from django.http import JsonResponse
# Create your views here.

@api_view(['POST'])
def echo(request):
    """
    Request json data and return it
    """
    if request.method == 'POST':
        data = request.data
        if data:
            return response(data, status=200, content_type=request.content_type)
        return response(status=status.HTTP_400_BAD_REQUEST)
    

class CustomXMLParser(BaseParser):
    """
    Custom XML parser, maybe user for later
    """
    media_type = 'application/xml'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as XML and returns the resulting data.
        """
        tree = ET.parse(stream)
        root = tree.getroot()
        return root
    


@api_view(['POST'])
@parser_classes([XMLParser])
def XMLDataCreate(request):
    """
    Request XML data and save to database
    """
    if request.method == 'POST':
        data = request.data
        if data:                
            if 'devices' in data and data['devices']: 
                # save the devices information
                for device_code,device_name in data['devices'].items():
                    device, created = Device.objects.get_or_create(code=device_code,
                                                                   name=device_name)
            

            if 'data' in data:
                for element in data['data']:
                    if 'device' in element and 'value' in element :
                        element_data={
                            'device':element['device'],
                            'value':element['value'],
                            'record_time':datetime.datetime.fromtimestamp(data['record_time']),
                            'data_id':data['id'],
                            }
                        serializer = ElementSerializer(data=element_data)
                        if serializer.is_valid():
                            serializer.save()
                            """
                            May use apscheduler to handle mass data
                            """
                            #scheduler.add_job(serializer.save(),) 
                        else:
                            response(serializer.errors,status=status.HTTP_424_FAILED_DEPENDENCY)            
                return response(status=status.HTTP_201_CREATED)
    return response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def XMLDataDisplay(request,id):
    """
    API to let client fetch the reformatted data by time
    """
    if request.method == 'GET':        
        serializer = ElementSerializer(Element.objects.filter(data_id=id).order_by('record_time'), many=True)
        return JsonResponse(serializer.data,json_dumps_params={'indent': 2}, safe=False)
    return response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def XMLDataList(request):
    """
    API to let client fetch the reformatted data by time
    """
    if request.method == 'GET':        
        serializer = ElementSerializer(Element.objects.all().order_by('record_time'), many=True)
        return JsonResponse(serializer.data,json_dumps_params={'indent': 2}, safe=False)
    return response(status=status.HTTP_400_BAD_REQUEST)

