from django.urls import path
from  django.conf.urls.static import static
from contentscour import settings

from . import views

urlpatterns = [
    path("api/", views.index, name="index"),
    path("api/chatbot/", views.chatbot),
    path("api/similarity_search/", views.similarity_search),
    path('api/document_upload/', views.document_upload),
    path('api/document_list/', views.document_list),
    path('api/document_delete/<int:pk>/', views.delete_document),
    path('api/document_process/<int:pk>/', views.process_document),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)