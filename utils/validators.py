from rest_framework import serializers


class CheckLinkVideo:

    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        link_video = data.get(self.field)
        if link_video and not link_video.startswith('https://www.youtube.com'):
            raise serializers.ValidationError(
                {self.field: 'Размещать видео-ссылки можно только с ресурсов youtube.com'}
            )
