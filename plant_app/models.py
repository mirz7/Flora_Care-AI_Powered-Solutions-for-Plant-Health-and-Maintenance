from django.db import models
from django.utils import timezone

class Plant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Device(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.device_id} - {self.plant.name}"

class SensorData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sensor_data')
    temperature = models.FloatField()
    humidity = models.FloatField()
    soil_moisture = models.IntegerField()
    last_watering = models.BigIntegerField(null=True, blank=True)
    automatic_watering = models.BooleanField(default=True)
    soil_threshold = models.IntegerField(default=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Data for {self.device.device_id} at {self.timestamp}"

class DeviceCommand(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='commands')
    water_plant = models.BooleanField(default=False)
    watering_duration = models.IntegerField(null=True, blank=True)
    update_settings = models.BooleanField(default=False)
    automatic_watering = models.BooleanField(null=True, blank=True)
    soil_threshold = models.IntegerField(null=True, blank=True)
    executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Command for {self.device.device_id}: {'Water' if self.water_plant else 'Settings update'}"
    
    def mark_as_executed(self):
        self.executed = True
        self.executed_at = timezone.now()
        self.save()