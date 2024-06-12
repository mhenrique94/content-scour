from .models import Document


def get_user_documents(user):
    docs = Document.objects.filter(user=user).values()
    return docs

