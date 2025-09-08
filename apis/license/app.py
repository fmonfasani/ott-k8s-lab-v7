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

@app.post("/license")
def license_issue():
    b = request.get_json(force=True) or {}
    if not b.get("contentId") or not b.get("deviceId"):
        return jsonify(ok=False, error="missing fields"), 400
    return jsonify(ok=True, licenseKey="ABC123-FAKE-KEY")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
