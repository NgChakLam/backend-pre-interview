"""echo api testing
"""
import os
import json
import datetime
import pytest
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


def sample_xml(id_value,time_value):
    """
    Generate XML data for testing
    """
    root = ET.Element("root")
    data = ET.SubElement(root, "data")   
    ET.SubElement(root, 'id').text = str(id_value)
    record_time=ET.SubElement(root, 'record_time')
    element = ET.SubElement(data, 'element')
    element_list={             
                'SGD-12344':'1234.266',
                'SGB-11233':'60',
                'SCC-525':'220',
                'SGC-1552':'5266.66',
                'SGB-11233':'440',
                'G3112':'32.266',
                'SGD-12344':'1234.266',
                }
    
    for d,v in element_list.items():
        ET.SubElement(element, 'device').text=d
        ET.SubElement(element, 'value').text=v
    
    devices = ET.SubElement(root, 'devices')

    device_list={
                'G3112':'Temperature Sensor',
                'SCC-525':'Voltage Meter',
                'SGB-11233':'Current Meter',
                'SGC-1552':'Power Meter',
                'SGD-12344':'Power Meter',
            }
    for code,name in device_list.items():   
        ET.SubElement(devices,code).text=name
     
    record_time.text=str(int(time_value.timestamp()))
    data= ET.tostring(root,encoding="unicode")       
    return data
    

class TestXMLDataCreate:
    @pytest.mark.django_db
    @given(
        #Code maybe use to generate random data(not complete)
        #device=st.text(min_size=1),
        #device_code=st.text(min_size=1),
        #value=st.decimals(),
        #no_of_element=st.integers(min_value=0),        
        time=st.datetimes(min_value=datetime.datetime(1970, 1, 2, 0),max_value=datetime.datetime(3002, 12, 31, 0, 0)),
        id=st.integers(min_value=1,max_value=10000),
           )

    def test_XMLDataCreate(self,time,id, rf):
        """Testing _XMLDataCreate api response status result is function correctly with xml data
        """
        xml_data = sample_xml(id_value=id,time_value=time)
        data='<?xml version="1.0" encoding="UTF-8"?>'+xml_data
        print('data:',data)
        request = rf.post('/data/', data, content_type='application/xml')
        response = XMLDataCreate(request)
        assert response.status_code == 201
        print(response.render())
        
class TestXMLDataDisplay:
    def test_XMLDataDisplay_json_status_result(self):
        """Testing _XMLDataDisplay api response status result is function correctly with json data
        """
        pass
        
        
