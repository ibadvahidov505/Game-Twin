import logging
import os  # Canlı server portunu dinamik tutmaq üçün lazımdır
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from analysis import analyze_player
from steam_service import get_steam_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)
    if not data:
        logger.warning("Invalid or missing JSON body")
        return jsonify({"error": "Request body must be valid JSON"}), 400

    genres = data.get("genres", [])
    hours_played = data.get("hours_played", 0)
    achievements = data.get("achievements", 0)
    steam_username = data.get("steam_username", "").strip()

    user = None
    if steam_username:
        user = get_steam_user(steam_username)
        if user:
            hours_played = user["hours_played"]
            logger.info("Using Steam user hours: %s", hours_played)

    logger.info("Analyzing player: genres=%s, hours=%s, achievements=%s", genres, hours_played, achievements)

    if steam_username and user and "analysis" in user:
        result = dict(user["analysis"])
    else:
        result = analyze_player(
            genres=genres,
            hours_played=hours_played,
            achievements=achievements,
        )

    if steam_username and user:
        result["steam_user"] = user

    logger.info("Result: %s", result)
    return jsonify(result), 200


@app.route("/api/steam-profile", methods=["POST"])
def steam_profile():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = data.get("steam_username", "").strip()
    if not username:
        return jsonify({"error": "steam_username is required"}), 400

    user = get_steam_user(username)
    if not user:
        return jsonify({"error": f"User '{username}' not found"}), 404

    analysis = user.get("analysis") or analyze_player(
        genres=data.get("genres", []),
        hours_played=user["hours_played"],
        achievements=data.get("achievements", 0),
    )

    return jsonify({
        "steam_user": user,
        "analysis": analysis,
    }), 200


# CANLI SERVER PORT TƏNZİMLƏMƏSİ
if __name__ == "__main__":
    # Railway-in verdiyi xüsusi portu oxuyur, tapmasa lokal üçün 5000-i işə salır
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)