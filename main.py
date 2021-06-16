from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from ingestor import youtube_ingestor
from functools import partial
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['youtube']
video_collection = db['videos']

youtube_ingestor_for_animals = partial(youtube_ingestor, "animals", video_collection)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(youtube_ingestor_for_animals, 'interval', seconds=10)
scheduler.start()

app = Flask(__name__)


@app.route('/videos')
def videos():
    offset = int(request.args.get('offset', default=0))
    size = int(request.args.get('size', default=30))
    q = request.args.get('q')

    return {
        'data': [

        ],
        'page': {
            'size': size,
            'offset': offset,
            'next': f"/videos?size={size}&offset={offset + size}"
        }

    }


if __name__ == "__main__":
    app.run()
