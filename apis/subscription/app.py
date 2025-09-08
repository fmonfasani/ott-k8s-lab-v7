from flask import Flask, request, jsonify
import jwt
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
SECRET = "super-secret-key"
metrics = PrometheusMetrics(app)

@app.get("/health")
def h():
    return ("ok", 200)

@app.get("/ready")
def r():
    return ("ok", 200)

@app.get("/subscription/check/<content_id>")
def check(content_id):
    try:
        token = request.headers.get("Authorization", "").split(" ")[1]
        jwt.decode(token, SECRET, algorithms=["HS256"])
        return jsonify(entitled=(content_id != "blocked123"))
    except Exception as e:
        return jsonify(error="unauthorized", detail=str(e)), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
