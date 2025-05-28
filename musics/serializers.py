# from rest_framework import serializers
# from .models import Song

# class SongSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Song
#         fields = ["id", "title", "album","audio_file", "cover_image", "artist"]
#         extra_kwargs={"user":{"read_only":True},"service":{"read_only":True}}