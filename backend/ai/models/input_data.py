import uuid
from django.db import models
from utils.base_model import BaseModel
from django.contrib.auth.backends import UserModel


class InputData(BaseModel):
    SOURCE = (
        ('YOUTUBE', 'YOUTUBE'),
        ('SPOTIFY', 'SPOTIFY'),
    )
    TRANSCRIPTION_TYPE = (
        ("GENERATED", "GENERATED"),
        ("MANUAL", "MANUAL"),
        ("LLM", "LLM"),
    )
    STATUS = (
        ("NEW", "NEW"),
        ("PROCESSING", "PROCESSING"),
        ("DONE", "DONE"),
        ("ERROR", "ERROR"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=25, choices=SOURCE, null=False)
    transcription_type = models.CharField(max_length=25, choices=TRANSCRIPTION_TYPE, null=False)
    audio_length = models.IntegerField(null=True, blank=True)
    source_title = models.CharField(max_length=255, null=True, blank=True)
    source_url = models.URLField(null=False)
    status = models.CharField(max_length=25, choices=STATUS, null=False, default="NEW")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
