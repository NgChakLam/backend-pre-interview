"""echo api testing
"""
import os
import json
from string import printable

from hypothesis import strategies as st
from hypothesis import given,example
from django.test import Client
import xml.etree.cElementTree as ET

from .views import echo, XMLDataCreate

json_data = st.recursive(st.booleans() | st.floats() | st.text(printable),
                        lambda children: st.dictionaries(st.text(printable), children))

class TestEcho:
    @given(json_data=json_data)
    def test_echo_json_status_result(self, json_data, rf):
        """Testing echo api response status result is function correctly with json data
        """
        data = {'null':json.dumps(json_data)}
        request = rf.post('/echo/', data, content_type='application/json')
        response = echo(request)
        assert response.status_code == 200
        response.render()
        assert response.data == data


def sample_xml(id_value):
    """
    Generate XML data for testing
    """
    root = ET.Element("root")
    data = ET.SubElement(root, "data")    
    
    id = ET.SubElement(root, 'id')
    id.text = str(id_value)
    record_time=ET.SubElement(root, 'record_time')
    element = ET.SubElement(data, 'element')
    device = ET.SubElement(element, 'device')
    
    value = ET.SubElement(element, 'value')
       
    
    devices = ET.SubElement(root, 'devices')
    device_code_list=['G3112','SCC-525','SGB-11233','SGC-1552','SGD-12344']
    device_name_list=['Temperature Sensor','Voltage Meter','Current Meter','Power Meter','Power Meter']
    for code in device_code_list:
        ET.SubElement(devices,code)
    data= ET.tostring(root,encoding="unicode")
    return data
    
    #print(tree)

    
#xml_data =  (device=st.text(min_size=1)))
            #'device':st.text(min_size=1),
            #'value':st.decimals(),
            #'no_of_element':st.integers(min_value=0),
            #'time':st.datetimes(),
            
workpath = os.path.dirname(os.path.abspath(__file__))
file = open(os.path.join(workpath, 'sample.xml'), 'r')
sample_xml=file.read()
print(sample_xml)
file.close()
    
class TestXMLDataCreate:
    """
    @given(
        device=st.text(min_size=1),
        #device_code=st.text(min_size=1),
        value=st.decimals(),
        no_of_element=st.integers(min_value=0),
        time=st.datetimes(),
        id=st.integers(min_value=1),
           )
    """
    #@example(xml_data=str(sample_xml))
    #def test_XMLDataCreate(self,device,value,no_of_element,time,id, rf):
    def test_XMLDataCreate(self,xml_data, rf):
        """Testing _XMLDataCreate api response status result is function correctly with xml data
        """
        
        #data='<?xml version="1.0" encoding="UTF-8"?>'+xml_data
        data=xml_data
        print('data:',data)
        request = rf.post('/data/', data, content_type='application/xml')
        response = XMLDataCreate(request)
        assert response.status_code == 201
        print(response.render())
        #import pytest
        #pytest.set_trace()
        
class TestXMLDataDisplay:
    def test_XMLDataDisplay_json_status_result(self):
        """Testing _XMLDataDisplay api response status result is function correctly with json data
        """
        pass
        
        
