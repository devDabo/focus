from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from datetime import datetime
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from transformers import T5Tokenizer, T5ForConditionalGeneration
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

CORS(app)
mongo = PyMongo(app)
db = mongo.db.study_sessions

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, top_n=5):
    doc = nlp(text)
    words = [token.text for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(words)
    common_words = word_freq.most_common(top_n)
    return ' '.join([word for word, _ in common_words])

def generate_summary_from_keywords(keywords):
    keywords_string = ' '.join(keywords)
    input_text = "summarize: " + keywords_string
    input_ids = tokenizer.encode(input_text, return_tensors="pt", add_special_tokens=True)
    summary_ids = model.generate(input_ids, max_length=50, min_length=5, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

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
    mood = request.json.get('mood')  # Get the mood from the request
    
    valid_moods = ["happy", "neutral", "sad", "angry"]
    if mood not in valid_moods:
        return jsonify(error="Invalid mood selected"), 400

    db.update_one({'_id': ObjectId(session_id)}, {
        "$push": {
            "intervals": {
                "summary": summary,
                "timestamp": datetime.utcnow(),
                "mood": mood  # Save the mood alongside the summary
            }
        }
    })
    return jsonify(message="Summary and mood submitted", session_id=session_id)

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
    session = db.find_one({'_id': ObjectId(session_id)})

    if session:
        detailed_text = " ".join([interval['summary'] for interval in session['intervals']])
        keywords = extract_keywords(detailed_text, top_n=10).split()
        summary = generate_summary_from_keywords(keywords)
        return jsonify(summary=summary)
    else:
        return jsonify(error="Session not found"), 404

if __name__ == "__main__":
    app.run(debug=True)