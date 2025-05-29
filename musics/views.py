from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from rest_framework.permissions import AllowAny
import requests

# Create your views here.
@api_view(["GET"])
@permission_classes([AllowAny])
def music(request, pk):
    
    track_id = pk

    url = "https://spotify-scraper.p.rapidapi.com/v1/track/metadata"

    
    querystring = {"trackId":track_id}

    headers = {
        "x-rapidapi-key": os.environ.get("x-rapidapi-key"),
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
        "x-rapidapi-key": os.environ.get("x-rapidapi-key"),
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
            print("No 'soundcloudTrack' or 'audio' key found")
    else:
        print("Failed to fetch data")

    return audio_details


@api_view(["POST"])
@permission_classes([AllowAny])
def search(request):
        # search_query = request.POST['search_query']
        search_query = request.data.get('search_query', '')

        url = "https://spotify-scraper.p.rapidapi.com/v1/search"

        querystring = {"term":search_query,"type":"track"}

        headers = {
            "X-RapidAPI-Key":os.environ.get("x-rapidapi-key"),
            "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        track_list = []

        if response.status_code == 200:
            data = response.json()

            search_results_count = data["tracks"]["totalCount"]
            tracks = data["tracks"]["items"]

            for track in tracks:
                track_name = track["name"]
                artist_name = track["artists"][0]["name"]
                duration = track["durationText"]
                trackid = track["id"]

                # if get_track_image(trackid, track_name):
                #     track_image = get_track_image(trackid, track_name)
                # else:
                #     track_image = "https://imgv3.fotor.com/images/blog-richtext-image/music-of-the-spheres-album-cover.jpg"

                track_list.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'duration': duration,
                    'trackid': trackid,
                    # 'track_image': track_image,
                })

            return Response({
                'search_results_count': search_results_count,
                'track_list': track_list,
            })
        return Response({"error": "Failed to fetch track metadata from Spotify Scraper."},
            status=response.status_code)

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def 

