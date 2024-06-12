from django.db import models
from pgvector.django import VectorField

class Document(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    vector = VectorField(
        dimensions=768,
        help_text="Vector embeddings (clip-vit-large-patch14) of the file content",
        null=True,
        blank=True
    )

    def to_serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'filename': self.filename,
            'file_type': self.file_type,
            'uploaded_at': self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'processed': self.processed,
        }