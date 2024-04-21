from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.input_data import InputData
from .sources.youtube_processor import YoutubeProcessor


@receiver(post_save, sender=InputData)
def run_youtube_processor(sender, instance, created, **kwargs):
    # TODO later change this and first set `instance.status = "PROCESSING"` and then
    # run the Celery task to process
    if created and instance.source == "YOUTUBE" and instance.status == "NEW":
        youtube_processor = YoutubeProcessor(instance)
        status = youtube_processor.process()
        instance.status = status
        instance.save()


post_save.connect(run_youtube_processor, sender=InputData)
