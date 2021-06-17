from flask import Flask, request
from ingestor import init_youtube_ingestor
from utils import make_cache_key
from pymongo import MongoClient
from bson.json_util import dumps
import json
from flask_caching import Cache

client = MongoClient('mongodb://localhost:27017/')
db = client['youtube']
video_collection = db['videos']
init_youtube_ingestor(video_collection, "animal", 5)

config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/videos')
@cache.cached(timeout=100000, key_prefix=make_cache_key)
def videos():
    offset = int(request.args.get('offset', default=0))
    size = int(request.args.get('size', default=30))
    q = request.args.get('q', default="")
    if q == "":
        db_result = video_collection.find({}).skip(offset).limit(size).sort('publishedat', -1)
        res = json.loads(dumps(list(db_result)))
    else:
        db_result = video_collection.find({"$text": {"$search": q}}).skip(offset).limit(size).sort('publishedat', -1)
        res = json.loads(dumps(list(db_result)))

    return {
        'data': res,
        'page': {
            'size': size,
            'offset': offset,
            'next': f"/videos?size={size}&offset={offset + size}"
        }

    }


if __name__ == "__main__":
    app.run()
