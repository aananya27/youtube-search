from flask import request
from pymongo import UpdateOne


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')


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
