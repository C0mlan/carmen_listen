import requests
import os


def get_audio_details(query):
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud"
    

    querystring = {"track": query}

    headers = {
        "x-rapidapi-key": os.environ.get("x_rapidapi_key"),
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