Here’s the updated `README.md` with an additional section for **Adding Environment Variables**, just like you described:

---

# **FloraCare - Smart Plant Monitoring & Community Platform**

**FloraCare** is an all-in-one smart plant care solution that combines **Machine Learning**, **IoT**, and a social **Community** platform to enhance the plant care experience for individuals and gardening enthusiasts.

---

## **Key Features**

### **1. Machine Learning-Based Plant Disease Detection**
- CNN model built with PyTorch 
- Supports 38 different plant classes.
- Identifies plant diseases from user-uploaded images.
- Powered by a custom-trained machine learning model.

### **2. Plant Guide Generator**
- Uses **Gemini API** to generate personalized care instructions.
- Offers tailored tips for each plant type detected.

### **3. IoT-Enabled Monitoring & Control**
- Integrated with **ESP32** microcontroller.
- Sensors: Temperature, Humidity, Soil Moisture.
- **Watering Pump Control**:
  - **Manual Control**: Toggle the pump through UI.
  - **Automatic Control**: Waters plants based on real-time soil moisture threshold.

### **4. Community Platform**
- User profiles for plant enthusiasts.
- Share posts (images of plants, doubts, stories) just like Instagram.
- Features include:
  - Like, comment, and reply on posts.
  - Share photos of diseased plants and get help from the community.

---

## **Demo**

Here’s a glimpse of how **FloraCare** works in real-time:

<a href="./demo/Flora_care.mp4">Video Link</a>
Or view the screenshots below:


- **IoT Setup**  
<a href="./demo/iot.jpg">Iot</a>
---

## **Tech Stack**
- **Backend**: Django
- **Frontend**: HTML, CSS, JS (Django templates)
- **IoT Module**: C++ on ESP32
- **Machine Learning**: CNN model built with PyTorch and integrated into Django
- **AI Guide**: Gemini API for care generation

---

## **How to Run the Project**

### **1. Clone the Repository**
```bash
git clone https://github.com/mirz7/floracare.git
cd floracare
```

### **2. Create & Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Adding Environment Variables**

### **Step 1: Rename `.test.env`**
Rename the provided `.test.env` file to `.env`:

```bash
mv .test.env .env
```

### **Step 2: Add the following keys to `.env`**

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

> Make sure the same keys are included in your environment-specific config files or deployment settings as needed.

---

## **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

## **Create Superuser**
```bash
python manage.py createsuperuser
```

## **Start the Server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## **ESP32 Code (IoT Module)**

The `iot/` folder contains:
- `main.cpp` – C++ code for ESP32 to read sensor data and control pump.
- Use Arduino IDE to flash it to your ESP32.

### **Required Libraries**
- `WiFi.h`
- `HTTPClient.h`
- DHT and Soil Moisture libraries

---

## **Contribution**
Pull requests are welcome. For major changes, open an issue first.

---

#   F l o r a _ C a r e - A I _ P o w e r e d - S o l u t i o n s - f o r - P l a n t - H e a l t h - a n d - M a i n t e n a n c e  
 