# FloraCare - AI powered Solutions For plant health and maintainance

FloraCare is an all-in-one smart plant care solution that combines Machine Learning**, IoT, and a social Community platform to enhance the plant care experience for individuals and gardening enthusiasts.


## Features :

1. Machine Learning-Based Plant Disease Detection

CNN model built with PyTorch
Supports 38 different plant classes
Provides instant plant health diagnostics
Trained on thousands of diverse plant leaf images
Identifies both common and rare plant diseases
Integrated directly with Django backend

2. Plant Guide Generator

Utilizes Gemini API for intelligent care instructions
Generates personalized watering schedules
Provides sunlight and soil recommendations
Offers treatment options for detected diseases
Includes preventative care measures
Adapts recommendations based on plant conditions
Delivers seasonal care tips

3. IoT-Enabled Monitoring & Control

ESP32 microcontroller integration
Temperature monitoring (-40°C to 80°C range)
Humidity tracking (0-100%)
Soil moisture measurement with calibrated thresholds
Manual watering activation via web interface
Automated watering based on customizable thresholds
Built-in failsafes to prevent overwatering
Scheduling capabilities for routine watering cycles
Real-time data visualization dashboard

4. Community Platform

Customizable user profiles for plant enthusiasts
Instagram-style feed for sharing plant content
Likes, nested comments, and replies on posts
Searchable plant care knowledge base
Mobile-responsive interface

## Demo

<a href="./demo/Flora_care.mp4">Video Link</a>


https://github.com/user-attachments/assets/e8b83002-8655-41de-a717-533f27c36f86


## Adding Environment Variables

- Rename the provided `.test.env` file to `.env`

```bash
mv .test.env .env
```

- Add the following keys to `.env`:

```env
# Google reCAPTCHA
GOOGLE_RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key

# Google Auth / Social Login
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# SMTP Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key
```

## Installation

```bash
    $ git clone https://github.com/mirz7/floracare.git
    $ cd floracare
    $ python -m venv venv
    $ source venv/bin/activate    # On Windows: venv\Scripts\activate
    (venv) pip install -r requirements.txt
    (venv) python manage.py makemigrations
    (venv) python manage.py migrate
    (venv) python manage.py createsuperuser
    (venv) python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## ESP32 Code (IoT Module)

The `iot/` folder contains:
- `main.cpp` – C++ code for ESP32 to read sensor data and control pump
- Use Arduino IDE to flash it to your ESP32

### Required Libraries
- `WiFi.h`
- `HTTPClient.h`
- DHT and Soil Moisture libraries

## Tech Stack
- **Backend**: Django
- **Frontend**: HTML, CSS, JS (Django templates)
- **IoT Module**: C++ on ESP32
- **Machine Learning**: CNN model built with PyTorch
- **AI Guide**: Gemini API

## Contribution
Pull requests are welcome. For major changes, open an issue first.#
