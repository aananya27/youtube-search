db = db.getSiblingDB("youtubedump");
db.videos.drop();
db.videos.createIndex({ "tile": "text", "description": "text" });
