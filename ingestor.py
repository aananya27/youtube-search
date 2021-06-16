from pymongo import UpdateOne
import requests


def youtube_ingestor(query_term, video_collection):
    key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
    youtube_content_url = f"https://content-youtube.googleapis.com/youtube/v3/search?part=snippet&key=" \
                          f"{key}&q={query_term}"
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
