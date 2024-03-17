from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://rajchand99:rajchand99@focus.1e9gpvt.mongodb.net/focus?retryWrites=true"

CORS(app)
mongo = PyMongo(app)

db = mongo.db.study_sessions

@app.route("/study/start", methods=["POST"])
def start_study_session():
    interval_duration = request.json.get('interval_duration')
    session_id = db.insert_one({
        "start_time": datetime.utcnow(),
        "end_time": None,
        "interval_duration": interval_duration,
        "interval": [],
        "status": "active"
    }).inserted_id
    return jsonify(message="Study session started", session_id=str(session_id))

@app.route("/study/stop", methods=["POST"])
def stop_study_session():
    session_id = request.json.get('session_id')
    db.update_one({'_id': ObjectId(session_id)}, {
        "$set": {"end_time": datetime.utcnow(), "status": "inactive"}
    })
    return jsonify(message="Study session stopped", session_id=session_id)

@app.route("/study/summary/submit", methods=["POST"])
def submit_interval_summary():
    session_id = request.json.get('session_id')
    summary = request.json.get('summary')
    db.update_one({'_id': ObjectId(session_id)}, {
        "$push": {"intervals": {"summary": summary, "timestamp": datetime.utcnow()}}
    })
    return jsonify(message="Summary submitted", session_id=session_id)

@app.route("/study/summaries/<session_id>", methods=["GET"])
def get_interval_summaries(session_id):
    session = db.find_one({'_id': ObjectId(session_id)}, {'_id': 0, 'intervals': 1})
    if session:
        return jsonify(session)
    else:
        return jsonify(error="Session not found"), 404

@app.route("/study/summary/generate", methods=["POST"])
def generate_llm_summary():
    session_id = request.json.get('session_id')
    session = db.find_one({'_id': ObjectId(session_id)}, {'_id': 0, 'intervals': 1})
    if session:
        # add method for LLM summary logic
        llm_summary = "LLM-generated summary based on the combined summaries."
        return jsonify(llm_summary=llm_summary)
    else:
        return jsonify(error="Session not found"), 404

if __name__ == "__main__":
    app.run(debug=True)