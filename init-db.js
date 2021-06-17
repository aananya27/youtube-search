db = db.getSiblingDB("youtubedump");
db.videos.drop();
db.videos.createIndex({ "title": "text", "description": "text" });
db.videos.createIndex({ "published_at" : -1});
