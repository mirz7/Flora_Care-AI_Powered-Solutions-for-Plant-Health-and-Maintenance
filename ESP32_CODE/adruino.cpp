//flash this code to your esp32

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <SPIFFS.h>

// WiFi credentials
const char* ssid = "";
const char* password = "";

// Django server details
const char* serverUrl = "http://<yourlocalip>:8000/"; // Change to your Django server IP/domain
const char* apiEndpoint = "plant-data/";  // Change to match your Django API endpoint
const char* deviceId = "esp32-475A24";        // Unique ID for this device
const int sendInterval = 30000;                // Send data every 60 seconds (adjust as needed)
unsigned long lastSendTime = 0;

// Pin definitions
#define DHTPIN 4       // Pin for DHT11 sensor
#define SOIL_SENSOR 32 // Soil moisture sensor on analog pin
#define PUMP_PIN 26    // Water pump relay (through transistor or level shifter)
#define LED_PIN 33      // Built-in LED for status indication

// DHT sensor setup
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Variables for automated watering
int soilThreshold = 2000;  // Default threshold for dry soil (adjust based on your sensor)
unsigned long lastWateringTime = 0;
const unsigned long wateringCooldown = 3600000; // 1 hour cooldown between automatic watering
bool automaticWatering = true;  // Enable/disable automatic watering
int wateringDuration = 5000;    // Default watering duration in milliseconds (5 seconds)

// Function to read sensor data
void readSensorData(float &temp, float &hum, int &soil) {
  temp = dht.readTemperature();
  hum = dht.readHumidity();
  soil = analogRead(SOIL_SENSOR);
  
  // Handle NaN readings from DHT
  if (isnan(temp)) temp = 0;
  if (isnan(hum)) hum = 0;
  
  Serial.println("Sensor readings:");
  Serial.println("Temperature: " + String(temp) + "°C");
  Serial.println("Humidity: " + String(hum) + "%");
  Serial.println("Soil Moisture: " + String(soil));
}

// Function to water the plant
void waterPlant(int duration) {
  if (duration <= 0) duration = wateringDuration;
  
  Serial.println("Watering plant for " + String(duration) + " milliseconds");
  digitalWrite(PUMP_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);  // Turn on LED during watering
  delay(duration);
  digitalWrite(PUMP_PIN, LOW);
  digitalWrite(LED_PIN, LOW);   // Turn off LED after watering
  
  time_t now;
  time(&now);
  lastWateringTime = now; 


 // Update last watering time
}

// Function to send data to Django server
void sendDataToDjango() {
  HTTPClient http;
  
  // Read sensor data
  float temperature;
  float humidity;
  int soilMoisture;
  readSensorData(temperature, humidity, soilMoisture);
  
  // Create JSON document
  DynamicJsonDocument doc(1024);
  doc["device_id"] = deviceId;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["soil_moisture"] = soilMoisture;
  doc["last_watering"] = lastWateringTime;
  doc["automatic_watering"] = automaticWatering;
  doc["soil_threshold"] = soilThreshold;
  
  // Serialize JSON to string
  String jsonData;
  serializeJson(doc, jsonData);
  
  // Begin HTTP POST request
  String url = String(serverUrl) + String(apiEndpoint);
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  // Send POST request
  int httpResponseCode = http.POST(jsonData);
  
  // Check response
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("HTTP Response code: " + String(httpResponseCode));
    Serial.println("Response: " + response);
    
    // Parse response for commands
    DynamicJsonDocument respDoc(1024);
    DeserializationError error = deserializeJson(respDoc, response);
    
    if (!error) {
      // Check for watering command
      if (respDoc.containsKey("water_plant") && respDoc["water_plant"].as<bool>()) {
        int wateringTime = respDoc.containsKey("watering_duration") ? 
                          respDoc["watering_duration"].as<int>() : wateringDuration;
        
        Serial.println("Received watering command from server");
        waterPlant(wateringTime);
      }
      
      // Check for settings updates
      if (respDoc.containsKey("update_settings") && respDoc["update_settings"].as<bool>()) {
        if (respDoc.containsKey("automatic_watering")) {
          automaticWatering = respDoc["automatic_watering"].as<bool>();
        }
        if (respDoc.containsKey("soil_threshold")) {
          soilThreshold = respDoc["soil_threshold"].as<int>();
        }
        if (respDoc.containsKey("watering_duration")) {
          wateringDuration = respDoc["watering_duration"].as<int>();
        }
        
        Serial.println("Updated settings from server:");
        Serial.println("Automatic watering: " + String(automaticWatering ? "Enabled" : "Disabled"));
        Serial.println("Soil threshold: " + String(soilThreshold));
        Serial.println("Watering duration: " + String(wateringDuration) + " ms");
      }
    }
  } else {
    Serial.println("Error on sending POST: " + String(httpResponseCode));
    
    // Print more details about the error
    if (httpResponseCode == -1) {
      Serial.println("Connection failed or server unreachable");
    } else if (httpResponseCode == 403) {
      Serial.println("CSRF verification failed - check Django @csrf_exempt setting");
    }
  }
  
  http.end();
}

// Function to check commands from Django server
void checkForCommands() {
  HTTPClient http;
  
  // Begin HTTP GET request for commands
  String url = String(serverUrl) + String(apiEndpoint) + "commands/" + String(deviceId);
  http.begin(url);
  http.setTimeout(10000);
  // Send GET request
  int httpResponseCode = http.GET();
  
  // Check response
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Command check - HTTP Response code: " + String(httpResponseCode));
    
    // Parse response for commands
    DynamicJsonDocument respDoc(1024);
    DeserializationError error = deserializeJson(respDoc, response);
    
    if (!error) {
      // Check for watering command
      if (respDoc.containsKey("water_plant") && respDoc["water_plant"].as<bool>()) {
        int wateringTime = respDoc.containsKey("watering_duration") ? 
                          respDoc["watering_duration"].as<int>() : wateringDuration;
        
        Serial.println("Received watering command from server");
        waterPlant(wateringTime);
      }
      
      // Check for settings updates
      if (respDoc.containsKey("update_settings") && respDoc["update_settings"].as<bool>()) {
        if (respDoc.containsKey("automatic_watering")) {
          automaticWatering = respDoc["automatic_watering"].as<bool>();
        }
        if (respDoc.containsKey("soil_threshold")) {
          soilThreshold = respDoc["soil_threshold"].as<int>();
        }
        if (respDoc.containsKey("watering_duration")) {
          wateringDuration = respDoc["watering_duration"].as<int>();
        }
        
        Serial.println("Updated settings from server:");
        Serial.println("Automatic watering: " + String(automaticWatering ? "Enabled" : "Disabled"));
        Serial.println("Soil threshold: " + String(soilThreshold));
        Serial.println("Watering duration: " + String(wateringDuration) + " ms");
      }
    }
  } else {
    Serial.println("Error checking commands: " + String(httpResponseCode));
  }
  
  http.end();
}

void setup() {
  Serial.begin(9600);
  
  // Initialize pins
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);
  
  // Initialize sensors
  dht.begin();
  
  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  // Wait for connection with timeout
  int connectionAttempts = 0;
  while (WiFi.status() != WL_CONNECTED && connectionAttempts < 20) {
    delay(500);
    Serial.print(".");
    connectionAttempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to WiFi");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    
    // Indicate successful connection with LED blink
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_PIN, HIGH);
      delay(200);
      digitalWrite(LED_PIN, LOW);
      delay(200);
    }
  } else {
    Serial.println("\nFailed to connect to WiFi");
    // Indicate connection failure with long LED blink
    digitalWrite(LED_PIN, HIGH);
    delay(1000);
    digitalWrite(LED_PIN, LOW);
  }
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Send data to Django server at regular intervals
  if (currentMillis - lastSendTime >= sendInterval) {
    if (WiFi.status() == WL_CONNECTED) {
      sendDataToDjango();
      lastSendTime = currentMillis;
    } else {
      // Reconnect to WiFi if disconnected
      Serial.println("WiFi disconnected. Reconnecting...");
      WiFi.begin(ssid, password);
      
      // Wait for reconnection with timeout
      int reconnectionAttempts = 0;
      while (WiFi.status() != WL_CONNECTED && reconnectionAttempts < 10) {
        delay(500);
        Serial.print(".");
        reconnectionAttempts++;
      }
      
      if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nReconnected to WiFi");
      } else {
        Serial.println("\nFailed to reconnect to WiFi");
      }
    }
  }
  
  // Check for commands from Django server every 10 seconds
  if ((currentMillis % 10000) < 100 && WiFi.status() == WL_CONNECTED) { // Check every 10 seconds
    checkForCommands();
  }
  
  // Automatic watering system
  if (automaticWatering) {
    // Read soil moisture
    int soil = analogRead(SOIL_SENSOR);
    
    // If soil moisture is below threshold, water the plant
    if (soil >= soilThreshold) {  // Higher value means drier soil with most sensors
      Serial.println("Soil is dry. Starting automatic watering.");
      waterPlant(wateringDuration);
    }
  }
  
  // Small delay to prevent CPU hogging
  delay(100);
}