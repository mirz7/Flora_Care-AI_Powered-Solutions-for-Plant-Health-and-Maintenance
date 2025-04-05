import os
from django.shortcuts import render
from django.conf import settings
from PIL import Image
import torchvision.transforms.functional as TF
import numpy as np
import torch
import pandas as pd
from .models import DiseaseInfo, SupplementInfo

# Import the CNN model
from .ml_model import CNN

# Load the model
model = CNN.CNN(39)
model.load_state_dict(torch.load(os.path.join(settings.BASE_DIR, 'plant_disease_app/ml_model/plant_disease_model_1_latest.pt')))
model.eval()

# Load disease and supplement info
disease_info = pd.read_csv(os.path.join(settings.BASE_DIR, 'plant_disease_app/ml_model/disease_info.csv'), encoding='cp1252')
supplement_info = pd.read_csv(os.path.join(settings.BASE_DIR, 'plant_disease_app/ml_model/supplement_info.csv'), encoding='cp1252')

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

def ai_engine(request):
    print("Index view called")
    return render(request, 'plant_disease_app/ai_engine.html')
# def ai_engine_page(request):
#     return render(request, 'index.html')

def submit(request):
    if request.method == 'POST':
        image = request.FILES['image']
        # Save the image
        image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
        
        # Make sure the directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        # Save the image
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Make prediction
        pred = prediction(image_path)
        
        # Get disease info
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        
        # Get supplement info
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        
        context = {
            'title': title,
            'desc': description,
            'prevent': prevent,
            'image_url': image_url,
            'pred': pred,
            'sname': supplement_name,
            'simage': supplement_image_url,
            'buy_link': supplement_buy_link
        }
        
        return render(request, 'plant_disease_app/submit.html', context)