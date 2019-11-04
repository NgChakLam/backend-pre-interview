from django.db import models

# Create your models here.
"""
class Data(models.Model):
    data_id= models.IntegerField('Data ID')    
    element = models.ManyToManyField('Element')
    #record_time = models.CharField('Record_time',max_length=20)
    record_time = models.DateTimeField('Record Time')
"""
   
class Element(models.Model):    
    device = models.CharField('Device', max_length=20,null=True)    
    value = models.FloatField('value')
    data_id= models.PositiveIntegerField('Data ID') 
    record_time = models.DateTimeField('Record Time')
    
    def  __str__(self):
        return '%s : %s :%s :%s' %(self.device, self.value, self.data_id , self.record_time  )
    
    def unit(self):
        try:
            device=Device.objects.get(code=self.device)
            return device.unit()
        except Device.DoesNotExist:
            return 'Unknown, Cannot found information of the device'
    
class Device(models.Model):
    code = models.CharField('Device Code', max_length=20,unique=True)
    name = models.CharField('Device Name', max_length=25,null=True)
    
    def __str__(self):
        return '%s : %s' %(self.code, self.name )
    
    def unit(self):
        if self.name == 'Temperature Sensor':
            return '°C'
        if self.name == 'Voltage Meter':
            return 'V'
        if self.name == 'Power Meter':
            return 'kWh'
        if self.name == 'Current Meter':
            return 'A'