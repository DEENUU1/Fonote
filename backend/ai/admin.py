from django.contrib import admin
from .models.input_data import InputData
from .models.result import Result
from .models.fragment import Fragment


class InputDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'transcription_type', 'audio_length', 'status', 'user')
    list_filter = ('status', 'source', 'transcription_type')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_type', 'input')
    list_filter = ('result_type',)


admin.site.register(InputData, InputDataAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Fragment)
