from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.get("/health")
def h():
    return ("ok", 200)

@app.get("/ready")
def r():
    return ("ok", 200)

@app.post("/cas/authorize")
def authorize():
    b = request.get_json(force=True) or {}
    return jsonify(allowed=b.get("tier") in ("premium", "gold"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
