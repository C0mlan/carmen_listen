from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests

# Create your views here.
@api_view(["GET"])
@permission_classes([AllowAny])
def music(request, pk):
    
    track_id = pk

    url = "https://spotify-scraper.p.rapidapi.com/v1/track/metadata"

    # querystring = {"trackId":"5ubHAQtKuFfiG4FXfLP804"}
    querystring = {"trackId":track_id}

    headers = {
        "x-rapidapi-key": "2b32171cfcmsh2b74ce12bb45e76p12c331jsnfb91640a9cfa",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code ==200:
        data= response.json()

        track_name = data.get("name")
        artists_list = data.get("artists", [])
        first_artist_name = artists_list[0].get("name") if artists_list else "No aritst found"
        audio_details_query = track_name + first_artist_name
        audio_details = get_audio_details(audio_details_query)
        audio_url = audio_details[0]
        duration_text = audio_details[1]

        return Response({
            "track_name": track_name,
            "first_artist": first_artist_name,
            "audio_url": audio_url,
            "duration_text": duration_text
        })
    return Response({"error": "Failed to fetch track metadata from Spotify Scraper."},
    status=response.status_code)

def get_audio_details(query):
    
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud"
    

    querystring = {"track": query}

    headers = {
        "x-rapidapi-key": "2b32171cfcmsh2b74ce12bb45e76p12c331jsnfb91640a9cfa",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    audio_details = []
    if response.status_code == 200:
        response_data = response.json()
        if "soundcloudTrack" in response_data and "audio" in response_data['soundcloudTrack']:
            audio_list = response_data['soundcloudTrack']['audio']
            if audio_list:
                first_audio_url = audio_list[0]['url']
                duration_text = audio_list[0]['durationText']

                audio_details.append(first_audio_url)
                audio_details.append(duration_text)
            else:
                print("No audio data availble")
        else:
            print("No 'youtubeVideo' or 'audio' key found")
    else:
        print("Failed to fetch data")

    return audio_details

# def search(request):