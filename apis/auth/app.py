from flask import Flask, request, jsonify
import jwt, datetime
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
SECRET = "super-secret-key"
metrics = PrometheusMetrics(app)

@app.get("/health")
def h():
    return ("ok", 200)

@app.post("/auth/login")
def login():
    d = request.get_json(force=True) or {}
    if d.get("username") == "user" and d.get("password") == "pass":
        tok = jwt.encode({"sub": "user", "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET, algorithm="HS256")
        return jsonify(token=tok)
    return jsonify(error="invalid"), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
