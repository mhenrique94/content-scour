import json
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests

AI_ENDPOINT = settings.AI_ENDPOINT
AI_MODEL_NAME = settings.AI_MODEL_NAME
AI_API_KEY = settings.AI_API_KEY
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {AI_API_KEY}"
}

@csrf_exempt
def index(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            payload = json.dumps({
                "model": AI_MODEL_NAME,
                "messages": [
                    {
                    "role": "user",
                    "content": query
                    }
                ],
                "max_tokens": 256,
                "temperature": 0.7
            })
            response = requests.request("POST", AI_ENDPOINT, headers=HEADERS, data=payload)
            json_resp = response.json()
            return JsonResponse(json_resp)
        return JsonResponse({})
    return render(request, 'index.html')


