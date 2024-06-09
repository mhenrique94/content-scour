import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
import requests
from core import ai_svc
from django.views.decorators.csrf import csrf_exempt


AI_ENDPOINT = settings.AI_ENDPOINT
AI_MODEL_NAME = settings.AI_MODEL_NAME
AI_API_KEY = settings.AI_API_KEY
AWAN_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {AI_API_KEY}"
}


@csrf_exempt
def index(request):
    return render(request, 'index.html')


@require_POST
def similarity_search(request):
    query = request.POST.get('query')
    if query:
        processed_query = ai_svc.similarity_search(query)
        json_resp = processed_query.json()
        return JsonResponse(json_resp)
    return JsonResponse({'message': 'Erro: Type something!'}, status=500)


@csrf_exempt
@require_POST
def chatbot(request):
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
        response = requests.request("POST", AI_ENDPOINT, headers=AWAN_HEADERS, data=payload)
        json_resp = response.json()
        return JsonResponse(json_resp)
    return JsonResponse({'message': 'Erro: Type something!'}, status=500)
