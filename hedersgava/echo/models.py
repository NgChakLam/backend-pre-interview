from django.db import models

# Create your models here.

class Data(models.Model):
    data_id= models.IntegerField('Data ID')    
    element = models.ManyToManyField('Element')
    #record_time = models.CharField('Record_time',max_length=20)
    record_time = models.DateTimeField('Record Time')
    
class Element(models.Model):
    #device = models.OneToOneField('Device',on_delete=models.CASCADE,)
    device = models.CharField('Device', max_length=20)    
    value = models.FloatField('value')
    data_id= models.PositiveIntegerField('Data ID') 
    record_time = models.DateTimeField('Record Time')
    def  __str__(self):
        return '%s : %s :%s :%s' %(self.device, self.value, self.data_id , self.record_time  )
    
class Device(models.Model):
    code = models.CharField('Device Code', max_length=20,unique=True)
    name = models.CharField('Device Name', max_length=25)
    #unit = models.CharField('unit')
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