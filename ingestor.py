from pymongo import UpdateOne
import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial


def youtube_ingestor(query_term, video_collection):
    key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
    current_date_time = datetime.datetime.utcnow()
    minutes_delta = datetime.timedelta(minutes=5)
    time_at_to_scrape = (current_date_time - minutes_delta).isoformat() + "Z"
    print(time_at_to_scrape)
    youtube_content_url = f"https://content-youtube.googleapis.com/youtube/v3/search?part=snippet&key=" \
                          f"{key}&q={query_term}&type=video&order=date&publishedAfter{time_at_to_scrape}&maxResults=50"

    headers = {
        'authority': 'content-youtube.googleapis.com',
        'x-origin': 'https://explorer.apis.google.com'
    }
    response = requests.request("GET", youtube_content_url, headers=headers)

    if response.status_code == 200 and response.json().get("kind") == "youtube#searchListResponse":
        operations = []
        for item in response.json()["items"]:
            operations.append(UpdateOne({"video_id": item["id"]["videoId"]}, {
                "$set": {
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "publishedat": item["snippet"]["publishedAt"] or item["snippet"]["publishTime"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    "channelid": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "video_id": item["id"]["videoId"],
                }
            }, upsert=True))

        video_collection.bulk_write(operations)
    else:
        print("failed to fetch youtube response, error -", response.status_code, response.json())


def init_youtube_ingestor(video_collection, search_term, seconds):
    youtube_ingestor_for_animals = partial(youtube_ingestor, search_term, video_collection)
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(youtube_ingestor_for_animals, 'interval', seconds=seconds)
    scheduler.start()
