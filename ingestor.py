import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
from constants import key
from utils import get_video_dict


def youtube_ingestor(query_term, video_collection):
    # takes current time and rewinds 5 minutes from it to fetch data from that as publishedAt
    current_date_time = datetime.datetime.utcnow()
    minutes_delta = datetime.timedelta(minutes=5)
    time_at_to_scrape = (current_date_time - minutes_delta).isoformat() + "Z"

    youtube_content_url = f"https://content-youtube.googleapis.com/youtube/v3/search?part=snippet&key=" \
                          f"{key}&q={query_term}&type=video&order=date&publishedAfter{time_at_to_scrape}&maxResults=50"

    headers = {
        'authority': 'content-youtube.googleapis.com',
        'x-origin': 'https://explorer.apis.google.com'
    }
    try:
        response = requests.request("GET", youtube_content_url, headers=headers)
        if response.status_code == 200 and response.json().get("kind") == "youtube#searchListResponse":
            operations = []
            for item in response.json()["items"]:
                operations = get_video_dict(item, operations)
            video_collection.bulk_write(operations)
        else:
            print("Failed to fetch a valid response- "
                  f"\nerror code:{response.status_code}\nerror response:{response.json()}")

    except Exception as e:
        print("An error occoured-", e)


def init_youtube_ingestor(video_collection, search_term, seconds):
    youtube_ingestor_for_animals = partial(youtube_ingestor, search_term, video_collection)
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(youtube_ingestor_for_animals, 'interval', seconds=seconds)
    scheduler.start()
