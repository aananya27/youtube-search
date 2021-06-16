from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from ingestor import youtube_ingestor

youtube_ingestor(query_term="cat")
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(youtube_ingestor, 'interval', seconds=10)
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
