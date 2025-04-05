from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from rest_framework import viewsets
from .models import Plant, Device, SensorData, DeviceCommand
from rest_framework import serializers
from django.http import JsonResponse, HttpResponse

# Serializers for the API
class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

class DeviceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCommand
        fields = '__all__'

# ViewSets for the API
class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

class DeviceCommandViewSet(viewsets.ModelViewSet):
    queryset = DeviceCommand.objects.all()
    serializer_class = DeviceCommandSerializer

# Web interface views
def dashboard(request):
    """Display the main dashboard with all devices"""
    plants = Plant.objects.all()
    devices = Device.objects.filter(is_active=True)
    
    # Get latest data for each device
    for device in devices:
        latest_data = SensorData.objects.filter(device=device).order_by('-timestamp').first()
        device.latest_data = latest_data
    
    context = {
        'plants': plants,
        'devices': devices,
    }
    return render(request, 'plant_app/dashboard.html', context)

def device_detail(request, device_id):
    """Display detailed view for a specific device"""
    device = get_object_or_404(Device, device_id=device_id)
    latest_data = SensorData.objects.filter(device=device).order_by('-timestamp').first()
    
    # Get historical data for charts
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    
    historical_data = SensorData.objects.filter(
        device=device,
        timestamp__gte=start_time,
        timestamp__lte=end_time
    ).order_by('timestamp')
    
    # Format data for charts
    timestamps = []
    temperatures = []
    humidities = []
    soil_moisture = []
    
    for data in historical_data:
        timestamps.append(data.timestamp.strftime('%H:%M'))
        temperatures.append(data.temperature)
        humidities.append(data.humidity)
        soil_moisture.append(data.soil_moisture)
    
    # Get pending commands
    pending_commands = DeviceCommand.objects.filter(device=device, executed=False)
    
    context = {
        'device': device,
        'plant': getattr(device, 'plant', None),  # Safer access to plant attribute
        'latest_data': latest_data,
        'timestamps': json.dumps(timestamps),
        'temperatures': json.dumps(temperatures),
        'humidities': json.dumps(humidities),
        'soil_moisture': json.dumps(soil_moisture),
        'pending_commands': pending_commands,
    }
    
    return render(request, 'plant_app/device_detail.html', context)

# AJAX endpoints for the web interface
@csrf_exempt
def send_water_command(request, device_id):
    """Send a command to water the plant"""
    if request.method == 'POST':
        try:
            device = Device.objects.get(device_id=device_id)
            
            # Handle both form data and JSON payload
            if request.body and request.content_type == 'application/json':
                data = json.loads(request.body)
                print("button clicked for watering, recieved : ",data)
                duration = data.get('duration', 5000)
            else:
                duration = request.POST.get('duration', 5000)
            
            # Create watering command
            command = DeviceCommand.objects.create(
                device=device,
                water_plant=True,
                watering_duration=int(duration),
                update_settings=False,
                executed=False
            )
            
            return JsonResponse({'status': 'success', 'message': 'Watering command sent'})
        except Device.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Device not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def update_settings(request, device_id):
    """Update device settings"""
    if request.method == 'POST':
        try:
            device = Device.objects.get(device_id=device_id)
            
            # Ensure request body is not empty and is valid JSON
            if not request.body:
                return JsonResponse({'status': 'error', 'message': 'Empty request body'}, status=400)
            
            data = json.loads(request.body)
            
            # Create settings update command
            command = DeviceCommand.objects.create(
                device=device,
                water_plant=False,
                update_settings=True,
                automatic_watering=data.get('automatic_watering'),
                soil_threshold=data.get('soil_threshold'),
                watering_duration=data.get('watering_duration'),
                executed=False
            )
            
            return JsonResponse({'status': 'success', 'message': 'Settings updated'})
        except Device.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Device not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def get_device_data(request, device_id):
    """Get latest device data"""
    try:
        device = Device.objects.get(device_id=device_id)
        latest_data = SensorData.objects.filter(device=device).order_by('-timestamp').first()
        
        if latest_data:
            # Calculate next possible watering time based on cooldown
            next_possible_watering = 0
            if latest_data.last_watering:
                try:
                    last_watering_time = datetime.fromtimestamp(latest_data.last_watering )
                    cooldown_end = last_watering_time + timedelta(hours=1)  # 1 hour cooldown
                    
                    if datetime.now() < cooldown_end:
                        remaining = (cooldown_end - datetime.now()).total_seconds()
                        next_possible_watering = int(remaining)
                except (ValueError, TypeError, OverflowError):
                    next_possible_watering = 0
            
            data = {
                'temperature': latest_data.temperature,
                'humidity': latest_data.humidity,
                'soilMoisture': latest_data.soil_moisture,
                'lastWatering': latest_data.last_watering,
                'automaticWatering': latest_data.automatic_watering,
                'soilThreshold': latest_data.soil_threshold,
                'nextPossibleWatering': next_possible_watering,
                'wateringDuration': 5000  # Default 5 seconds
            }
            
            return JsonResponse(data)
        else:
            return JsonResponse({'status': 'error', 'message': 'No data available'}, status=404)
    except Device.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Device not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# ESP32 API endpoints
@csrf_exempt
def receive_plant_data(request):
    """Receive sensor data from ESP32 devices"""
    if request.method == 'POST':
        try:
            # Ensure request contains data
            if not request.body:
                return JsonResponse({'status': 'error', 'message': 'Empty request body'}, status=400)
                
            data = json.loads(request.body)

            print("DATA RECIEVED FROM DEVICE ", data)
            device_id = data.get('device_id')
            
            if not device_id:
                return JsonResponse({'status': 'error', 'message': 'Missing device_id'}, status=400)
            
            # Get or create the device
            try:
                device = Device.objects.get(device_id=device_id)
            except Device.DoesNotExist:
                # Auto-register new device
                print("creating device")
                device = Device.objects.create(
                    device_id=device_id,
                    is_active=True
                )
                print("created device")
            
            # Create new sensor data entry
            sensor_data = SensorData.objects.create(
                device=device,
                temperature=data.get('temperature', 0),
                humidity=data.get('humidity', 0),
                soil_moisture=data.get('soil_moisture', 0),
                last_watering=data.get('last_watering', 0),
                automatic_watering=data.get('automatic_watering', True),
                soil_threshold=data.get('soil_threshold', 2000),
                timestamp=datetime.now()
            )
            
            # Check if there are any pending commands for this device
            response_data = {'status': 'success'}
            
            pending_commands = DeviceCommand.objects.filter(device=device, executed=False)
            if pending_commands.exists():
                command = pending_commands.first()
                
                if command.water_plant:
                    response_data['water_plant'] = True
                    response_data['watering_duration'] = command.watering_duration
                
                if command.update_settings:
                    response_data['update_settings'] = True
                    if command.automatic_watering is not None:
                        response_data['automatic_watering'] = command.automatic_watering
                    if command.soil_threshold:
                        response_data['soil_threshold'] = command.soil_threshold
                    if command.watering_duration:
                        response_data['watering_duration'] = command.watering_duration
                
                # Mark command as executed
                command.executed = True
                command.save()
            
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            print(str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def device_commands(request, device_id):
    """Serve commands to ESP32 devices"""
    if request.method == 'GET':
        try:
            device = Device.objects.get(device_id=device_id)
            pending_commands = DeviceCommand.objects.filter(device=device, executed=False)
            
            response_data = {}
            
            if pending_commands.exists():
                command = pending_commands.first()
                
                if command.water_plant:
                    response_data['water_plant'] = True
                    response_data['watering_duration'] = command.watering_duration
                
                if command.update_settings:
                    response_data['update_settings'] = True
                    if command.automatic_watering is not None:
                        response_data['automatic_watering'] = command.automatic_watering
                    if command.soil_threshold:
                        response_data['soil_threshold'] = command.soil_threshold
                    if command.watering_duration:
                        response_data['watering_duration'] = command.watering_duration
                
                # Mark command as executed
                command.executed = True
                command.save()
            
            return JsonResponse(response_data)
        except Device.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Device not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def test_view(request):
    return HttpResponse("Test view works!")