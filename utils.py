from flask import request
from pymongo import UpdateOne
from constants import DEFAULT_PAGE_OFFSET, DEFAULT_PAGE_SIZE

def make_cache_key(*args, **kwargs):
    offset = int(request.args.get('offset', default=DEFAULT_PAGE_OFFSET))
    size = int(request.args.get('size', default=DEFAULT_PAGE_SIZE))
    q = request.args.get('q', default="")
    return str(offset) + str(size) + q


def get_video_dict(item, operations):
    operations.append(UpdateOne({"video_id": item["id"]["videoId"]}, {
        "$set": {
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "published_at": item["snippet"]["publishedAt"] or item["snippet"]["publishTime"],
            "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
            "channel_id": item["snippet"]["channelId"],
            "channel_title": item["snippet"]["channelTitle"],
            "video_id": item["id"]["videoId"],
        }
    }, upsert=True))
    return operations
