from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

CDN = "http://cdn-edge-service.ott-platform.svc.cluster.local"
LICENSE = "http://license-api-service.ott-platform.svc.cluster.local/license"

@app.get("/health")
def h():
    return ("ok", 200)

@app.get("/catalog/<cid>")
def c(cid):
    return jsonify(contentId=cid, manifestUrl=f"{CDN}/media/demo/master.m3u8", licenseServerUrl=LICENSE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
