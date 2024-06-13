import json
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import render
import requests

from core.files_svc import get_user_documents
from .models import Document
from core import ai_svc
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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
def rag_from_query(request):
    query = request.POST.get('query')
    user = request.user
    if query:
        processed_query = ai_svc.rag_from_query(query, user)
        return JsonResponse(processed_query)
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



@login_required
@require_POST
def document_upload(request):
    user_files = request.FILES.getlist('files')
    for file in user_files:
        if file.content_type not in ['text/csv', 'application/pdf', 'text/plain']:
            return HttpResponseBadRequest('Tipo de arquivo não suportado.')

        filename, file_type = os.path.splitext(file.name)
        Document.objects.create(
            user=request.user,
            file=file,
            filename=filename,
            file_type=file_type.replace(".", "")
        )
    documents = get_user_documents(request.user)
    return JsonResponse({'documents': list(documents)})


@login_required
def document_list(request):
    documents = get_user_documents(request.user)
    return JsonResponse({'documents': list(documents)})


@login_required
def delete_document(request, pk):
    document = Document.objects.get(pk=pk)
    user = request.user
    if document.user == user:
        ai_svc.delete_user_document(document, user)
        documents = get_user_documents(user)
        return JsonResponse({'documents': list(documents)})
    else:
        return HttpResponseBadRequest('Exclusion denied.')


@login_required
def process_document(request, pk):
    document = Document.objects.get(pk=pk)
    user = request.user
    if document.user == user:
        ai_svc.process_user_document(document, user)
        documents = get_user_documents(user)
        return JsonResponse({'documents': list(documents)})
    else:
        return HttpResponseBadRequest('Você não tem permissão para processar este arquivo.')