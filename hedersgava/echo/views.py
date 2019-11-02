from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response as response
#from rest_framework_xml.parsers import XMLParser
from echo.parsers import XMLParser
from rest_framework.parsers import BaseParser
import datetime
# Create your views here.
#from django.http import JsonResponse
from echo.models import Device
from echo.serializers import DataSerializer,ElementSerializer#,DeviceSerializer
import xml.etree.cElementTree as ET

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
    Custom XML parser
    """
    media_type = 'application/xml'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as XML and returns the resulting data.
        """
        tree = ET.parse(stream)
        root = tree.getroot()
        for child in root:
            print(child.tag, child.attrib)
        for element in root.iter('data'):
            print(element)
        for element in root.findall('element'):
            value = element.get('value')
            device = element.get('device')
            print(value,device)
        return root
    


@api_view(['POST'])
@parser_classes([XMLParser])
def echoXML(request):
    """
    Request XML data and save to database
    """
    if request.method == 'POST':
        data = request.data
        

        print('data\n',data)
        #tree = ET.parse(data)
        #root = ET.fromstring(country_data_as_string)
        if data:        
            # save the devices information   
            if 'devices' in data: 
                for device_code,device_name in data['devices'].items():
                    device, created = Device.objects.get_or_create(code=device_code,name=device_name)
                    #print(device.name,device.unit())
                  
            if 'data' in data:    
                print(data)
                print(data['data'])
                for element in data['data']:
                    print(element)
                    element_data={
                        'device':element['device'],
                        'value':element['value'],
                        'record_time':datetime.datetime.fromtimestamp(data['record_time']),
                        'data_id':data['id'],
                        }
                    #print(element_data)
                    serializer = ElementSerializer(data=element_data)
                    #print(serializer)
                    if serializer.is_valid():
                        serializer.save()
                        print('serializer valid')
                    else:
                        print(serializer.errors)
        return response(data, status=200, content_type=request.content_type)
    return response(status=status.HTTP_400_BAD_REQUEST)

