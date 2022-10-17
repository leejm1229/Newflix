from django.db import models

class Youtube(models.Model):
    title = models.TextField(blank=True, null=True)
    sub_text = models.TextField(blank=True, null=True)
    channel = models.TextField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    start = models.TextField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube'


class YoutubeReal(models.Model):
    title = models.TextField(blank=True, null=True)
    sub_text = models.TextField(blank=True, null=True)
    channel = models.TextField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    start = models.TextField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_real'