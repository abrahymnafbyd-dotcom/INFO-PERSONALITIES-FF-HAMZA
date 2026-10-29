
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

API_NAME = "INFO PERSONALITIES FF HAMZA"
API_VERSION = "1.0.0"

PERSONALITIES = {
    "shotgun": {
        "name": "SHOTGUN",
        "description": "تركيبة مقترحة للقتال القريب",
        "characters": [
            {
                "name": "Tatsuya",
                "skill": "اندفاع سريع للوصول للخصم"
            },
            {
                "name": "Jota",
                "skill": "استعادة HP وفق شروط المهارة"
            },
            {
                "name": "D-Bee",
                "skill": "تحسين الحركة والدقة أثناء إطلاق النار"
            },
            {
                "name": "Hayato",
                "skill": "زيادة اختراق الدرع مع انخفاض HP"
            }
        ]
    },

    "awm": {
        "name": "AWM",
        "description": "تركيبة مقترحة للقنص",
        "characters": [
            {
                "name": "Maro",
                "skill": "زيادة الضرر حسب المسافة"
            },
            {
                "name": "Rafael",
                "skill": "تقليل صوت القنص وإخفاء موقعك"
            },
            {
                "name": "Moco",
                "skill": "تحديد الخصم بعد إصابته"
            },
            {
                "name": "Laura",
                "skill": "تحسين دقة التصويب أثناء استخدام المنظار"
            }
        ]
    },

    "headshot": {
        "name": "HEADSHOT",
        "description": "تركيبة مقترحة للتصويب على الرأس",
        "characters": [
            {
                "name": "Alok",
                "skill": "زيادة الحركة واستعادة HP"
            },
            {
                "name": "D-Bee",
                "skill": "تحسين الحركة والدقة أثناء إطلاق النار"
            },
            {
                "name": "Laura",
                "skill": "تحسين دقة التصويب بالمنظار"
            },
            {
                "name": "Hayato",
                "skill": "زيادة اختراق الدرع مع انخفاض HP"
            }
        ]
    },

    "rush": {
        "name": "RUSH",
        "description": "تركيبة مقترحة للهجوم السريع",
        "characters": [
            {
                "name": "Tatsuya",
                "skill": "اندفاع سريع"
            },
            {
                "name": "Jota",
                "skill": "استعادة HP وفق شروط المهارة"
            },
            {
                "name": "D-Bee",
                "skill": "تحسين الحركة والدقة"
            },
            {
                "name": "Sonia",
                "skill": "حماية وفق شروط المهارة"
            }
        ]
    },

    "ranked": {
        "name": "RANKED",
        "description": "تركيبة مقترحة للعب المتوازن",
        "characters": [
            {
                "name": "Alok",
                "skill": "زيادة الحركة واستعادة HP"
            },
            {
                "name": "Jota",
                "skill": "استعادة HP وفق شروط المهارة"
            },
            {
                "name": "Moco",
                "skill": "تحديد الخصم بعد إصابته"
            },
            {
                "name": "Hayato",
                "skill": "زيادة اختراق الدرع مع انخفاض HP"
            }
        ]
    }
}


def response(data, status=200):
    return jsonify({
        "api": API_NAME,
        "version": API_VERSION,
        "success": status == 200,
        "data": data
    }), status


@app.route("/", methods=["GET"])
def home():
    return response({
        "message": "API is online",
        "name": API_NAME,
        "version": API_VERSION,
        "documentation": "/api/v1"
    })


@app.route("/health", methods=["GET"])
def health():
    return response({
        "status": "online",
        "time": datetime.now(timezone.utc).isoformat()
    })


@app.route("/api/v1", methods=["GET"])
def documentation():
    return response({
        "endpoints": [
            "/",
            "/health",
            "/api/v1/personalities",
            "/api/v1/personalities/<type>"
        ],
        "types": list(PERSONALITIES.keys())
    })


@app.route("/api/v1/personalities", methods=["GET"])
def all_personalities():
    return response({
        "count": len(PERSONALITIES),
        "personalities": PERSONALITIES
    })


@app.route("/api/v1/personalities/<personality_type>", methods=["GET"])
def get_personality(personality_type):
    personality_type = personality_type.lower().strip()

    if personality_type not in PERSONALITIES:
        return response({
            "error": "Personality not found",
            "available": list(PERSONALITIES.keys())
        }, 404)

    return response(PERSONALITIES[personality_type])


@app.errorhandler(404)
def not_found(error):
    return response({"error": "Endpoint not found"}, 404)


@app.errorhandler(500)
def server_error(error):
    return response({"error": "Internal server error"}, 500)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )

