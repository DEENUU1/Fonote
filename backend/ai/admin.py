from django.contrib import admin
from .models import InputData


class InputDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'transcription_type', 'audio_length', 'status', 'user')
    list_filter = ('status', 'source', 'transcription_type')


admin.site.register(InputData, InputDataAdmin)
