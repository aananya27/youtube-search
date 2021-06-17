from flask import Flask, request
from ingestor import init_youtube_ingestor
from utils import make_cache_key
from pymongo import MongoClient
from bson.json_util import dumps
import json
from flask_caching import Cache
from constants import flask_app_config, CACHE_TIMEOUT_MS, INGESTOR_INTERVAL_SECONDS, DEFAULT_PAGE_SIZE, DEFAULT_PAGE_OFFSET

# mongodb client init
client = MongoClient(host="test_mongodb", port=27017,
                     username='root',
                     password='pass',
                     authSource="admin")

# grab the video collection
db = client['youtubedump']
video_collection = db['videos']

# invoke youtube ingestor
init_youtube_ingestor(video_collection, "animal", INGESTOR_INTERVAL_SECONDS)

# create flask app with cache
app = Flask(__name__)
app.config.from_mapping(flask_app_config)
cache = Cache(app)


@app.route('/videos')
@cache.cached(timeout=CACHE_TIMEOUT_MS, key_prefix=make_cache_key)
def videos():
    # defined offset, size for pagination. query string for text search over title & description.
    offset = int(request.args.get('offset', default=DEFAULT_PAGE_OFFSET))
    size = int(request.args.get('size', default=DEFAULT_PAGE_SIZE))
    q = request.args.get('q', default="")
    try:
        if q == "":
            db_result = video_collection.find({}).skip(offset).limit(size).sort('published_at', -1)
        else:
            db_result = video_collection.find({"$text": {"$search": q}}).skip(offset).limit(size).sort('published_at',
                                                                                                       -1)
        if db_result:
            res = json.loads(dumps(list(db_result)))
        else:
            res = []
    except Exception as e:
        print("An error occoured while reading from the database", e)
        return 'Something went wrong', 500

    return {
        'data': res,
        'page': {
            'size': size,
            'offset': offset,
            # gives the path for next page, if list is exhausted null is set for frontend to detect
            'next': None if len(res) < size else f"/videos?size={size}&offset={offset + size}"
        }
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
