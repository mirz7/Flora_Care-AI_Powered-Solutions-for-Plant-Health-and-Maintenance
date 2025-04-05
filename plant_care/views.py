# import json
# import os
# import requests
# import logging
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Set up logging
# logger = logging.getLogger(__name__)

# # Home view for plant care
# @login_required
# def plant_care_home(request):
#     """
#     Renders the plant care home page.
#     """
#     return render(request, 'plant_care_home/plant_care_home.html')

# # View to generate a plant care guide
# @login_required
# def generate_care_guide(request):
#     """
#     Handles POST requests to generate a plant care guide using the Gemini API.
#     """
#     if request.method == 'POST':
#         plant_name = request.POST.get('plant_name', '').strip()
        
#         # Validate plant name
#         if not plant_name:
#             logger.error("Plant name is required")
#             return JsonResponse({'error': 'Plant name is required'}, status=400)
        
#         # Get care guide from Gemini API
#         care_guide = get_plant_care_guide(plant_name)
        
#         # Handle API errors
#         if 'error' in care_guide:
#             logger.error(f"Error in get_plant_care_guide: {care_guide['error']}")
#             return JsonResponse(care_guide, status=500)
        
#         # Return the care guide as JSON
#         return JsonResponse(care_guide)
    
#     # Handle invalid request methods
#     logger.error("Invalid request method")
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# # Helper function to fetch plant care guide from Gemini API
# def get_plant_care_guide(plant_name):
#     """
#     Fetches a plant care guide from the Gemini API.
#     """
#     try:
#         # Gemini API endpoint
#         api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
#         # Get API key from environment variables
#         api_key = os.getenv('GEMINI_API_KEY')
        
#         if not api_key:
#             logger.error("API key not found")
#             return {'error': 'API key not found'}
        
#         # Construct the URL with API key
#         url = f"{api_url}?key={api_key}"
        
#         # Format the prompt to get structured JSON output
#         prompt = f'''
#         Generate a detailed care guide for {plant_name} in valid JSON format.
#         Your response must be a properly formatted JSON object with NO additional text before or after.
        
#         Structure the response exactly as follows:
#         {{
#             "plant_name": "{plant_name}",
#             "soil_requirements": "Detailed soil requirements",
#             "water_requirements": "Detailed watering instructions",
#             "light_requirements": "Light needs and preferences",
#             "temperature_requirements": "Ideal temperature range and conditions",
#             "nutrient_requirements": "Fertilization needs and schedule",
#             "general_care_tips": "Additional care information",
#             "common_issues": "Common problems and solutions"
#         }}
        
#         Ensure your response is ONLY the JSON object and no other text.
#         '''
        
#         # Request payload
#         payload = {
#             "contents": [{
#                 "parts": [{
#                     "text": prompt
#                 }]
#             }],
#             "generationConfig": {
#                 "temperature": 0.2,
#                 "topP": 0.8,
#                 "topK": 40,
#                 "maxOutputTokens": 1024,
#             }
#         }
        
#         # Headers
#         headers = {
#             "Content-Type": "application/json"
#         }
        
#         # Make the API request
#         response = requests.post(url, json=payload, headers=headers)
        
#         # Check if the request was successful
#         if response.status_code == 200:
#             response_data = response.json()
            
#             # Extract the JSON content from the response
#             content_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
            
#             # Find the JSON object in the response
#             json_start = content_text.find('{')
#             json_end = content_text.rfind('}') + 1
            
#             if json_start != -1 and json_end != -1:
#                 json_string = content_text[json_start:json_end]
                
#                 try:
#                     # Try to parse the JSON string
#                     care_guide = json.loads(json_string)
                    
#                     # Validate that all required fields are present
#                     required_fields = [
#                         "plant_name", "soil_requirements", "water_requirements", 
#                         "light_requirements", "temperature_requirements", 
#                         "nutrient_requirements", "general_care_tips", "common_issues"
#                     ]
                    
#                     # Add any missing fields
#                     for field in required_fields:
#                         if field not in care_guide:
#                             care_guide[field] = f"Information not available for {field.replace('_', ' ')}"
                    
#                     return care_guide
#                 except json.JSONDecodeError as e:
#                     logger.error(f"JSON decode error: {e}")
#                     logger.error(f"Attempted to parse: {json_string}")
#                     return {'error': 'Failed to parse JSON from API response', 'details': str(e)}
#             else:
#                 logger.error(f"Could not find JSON in: {content_text}")
#                 return {'error': 'Could not extract JSON from API response'}
#         else:
#             logger.error(f"API request failed: {response.status_code}")
#             logger.error(f"Response content: {response.text}")
#             return {'error': f'API request failed with status code {response.status_code}'}
    
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Network error: {e}")
#         return {'error': f'Network error: {str(e)}'}
#     except Exception as e:
#         logger.error(f"Exception in get_plant_care_guide: {e}")
#         return {'error': f'An error occurred: {str(e)}'}
    
# import json
# import os
# import requests
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# @login_required
# def plant_care_home(request):
#     return render(request, 'plant_care/plant_care_home.html')

# @login_required
# def generate_care_guide(request):
#     if request.method == 'POST':
#         plant_name = request.POST.get('plant_name', '')
        
#         if not plant_name:
#             return JsonResponse({'error': 'Plant name is required'}, status=400)
        
#         # Get care guide from Gemini API
#         care_guide = get_plant_care_guide(plant_name)
        
#         if 'error' in care_guide:
#             return JsonResponse(care_guide, status=500)
        
#         return JsonResponse(care_guide)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# def get_plant_care_guide(plant_name):
#     try:
#         # Gemini API endpoint
#         api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
#         # Get API key from environment variables
#         api_key = os.getenv('GEMINI_API_KEY')
        
#         if not api_key:
#             return {'error': 'API key not found'}
        
#         # Construct the URL with API key
#         url = f"{api_url}?key={api_key}"
        
#         # Format the prompt to get structured JSON output
#         prompt = f'''
#         Generate a detailed care guide for {plant_name} in JSON format.
#         Structure the response as follows:
#         {{
#             "plant_name": "{plant_name}",
#             "soil_requirements": "Detailed soil requirements",
#             "water_requirements": "Detailed watering instructions",
#             "light_requirements": "Light needs and preferences",
#             "temperature_requirements": "Ideal temperature range and conditions",
#             "nutrient_requirements": "Fertilization needs and schedule",
#             "general_care_tips": "Additional care information",
#             "common_issues": "Common problems and solutions"
#         }}
#         '''
        
#         # Request payload
#         payload = {
#             "contents": [{
#                 "parts": [{
#                     "text": prompt
#                 }]
#             }]
#         }
        
#         # Headers
#         headers = {
#             "Content-Type": "application/json"
#         }
        
#         # Make the API request
#         response = requests.post(url, json=payload, headers=headers)
        
#         # Check if the request was successful
#         if response.status_code == 200:
#             response_data = response.json()
            
#             # Extract the JSON content from the response
#             content_text = response_data['candidates'][0]['content']['parts'][0]['text']
            
#             # Find the JSON object in the response
#             json_start = content_text.find('{')
#             json_end = content_text.rfind('}') + 1
            
#             if json_start != -1 and json_end != -1:
#                 json_string = content_text[json_start:json_end]
#                 care_guide = json.loads(json_string)
#                 return care_guide
#             else:
#                 return {'error': 'Could not extract JSON from API response'}
#         else:
#             return {'error': f'API request failed with status code {response.status_code}'}
    
#     except Exception as e:
#         return {'error': f'An error occurred: {str(e)}'}
import json
import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@login_required
def plant_care_home(request):
    return render(request, 'plant_care/plant_care_home.html')

@login_required
def generate_care_guide(request):
    if request.method == 'POST':
        plant_name = request.POST.get('plant_name', '')
        
        if not plant_name:
            return JsonResponse({'error': 'Plant name is required'}, status=400)
        
        # Get care guide from Gemini API
        care_guide = get_plant_care_guide(plant_name)
        
        if 'error' in care_guide:
            return JsonResponse(care_guide, status=500)
        
        return JsonResponse(care_guide)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_plant_care_guide(plant_name):
    try:
        # Gemini API endpoint
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        # Get API key from environment variables
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            return {'error': 'API key not found'}
        
        # Construct the URL with API key
        url = f"{api_url}?key={api_key}"
        
        # Format the prompt to get structured JSON output with explicit instructions
        prompt = f'''
        Generate a detailed care guide for {plant_name} in valid JSON format.
        Your response must be a properly formatted JSON object with NO additional text before or after.
        
        Structure the response exactly as follows:
        {{
            "plant_name": "{plant_name}",
            "soil_requirements": "Detailed soil requirements",
            "water_requirements": "Detailed watering instructions",
            "light_requirements": "Light needs and preferences",
            "temperature_requirements": "Ideal temperature range and conditions",
            "nutrient_requirements": "Fertilization needs and schedule",
            "general_care_tips": "Additional care information",
            "common_issues": "Common problems and solutions"
        }}
        
        Ensure your response is ONLY the JSON object and no other text.
        '''
        
        # Request payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.2,  # Lower temperature for more predictable output
                "topP": 0.8,
                "topK": 40,
                "maxOutputTokens": 1024,
            }
        }
        
        # Headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Make the API request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            
            # For debugging - log the full response
            print("Full Gemini API response:", response_data)
            
            # Extract the JSON content from the response
            content_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Find the JSON object in the response
            json_start = content_text.find('{')
            json_end = content_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_string = content_text[json_start:json_end]
                
                try:
                    # Try to parse the JSON string
                    care_guide = json.loads(json_string)
                    
                    # Validate that all required fields are present
                    required_fields = [
                        "plant_name", "soil_requirements", "water_requirements", 
                        "light_requirements", "temperature_requirements", 
                        "nutrient_requirements", "general_care_tips", "common_issues"
                    ]
                    
                    # Add any missing fields
                    for field in required_fields:
                        if field not in care_guide:
                            care_guide[field] = f"Information not available for {field.replace('_', ' ')}"
                    
                    return care_guide
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Attempted to parse: {json_string}")
                    return {'error': 'Failed to parse JSON from API response', 'details': str(e)}
            else:
                print("Could not find JSON in:", content_text)
                return {'error': 'Could not extract JSON from API response'}
        else:
            print(f"API request failed: {response.status_code}")
            print(f"Response content: {response.text}")
            return {'error': f'API request failed with status code {response.status_code}'}
    
    except Exception as e:
        import traceback
        print(f"Exception in get_plant_care_guide: {str(e)}")
        print(traceback.format_exc())
        return {'error': f'An error occurred: {str(e)}'}