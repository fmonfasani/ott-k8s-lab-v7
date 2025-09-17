
from fastapi import FastAPI
import os, requests, json

app = FastAPI(title="OTT Troubleshooting AI API", version="0.1.0")
PROM = os.getenv("PROM_URL", "http://prometheus.monitoring:9090")

def prom_query(expr: str) -> float:
    try:
        r = requests.get(f"{PROM}/api/v1/query", params={"query": expr}, timeout=5)
        r.raise_for_status()
        data = r.json().get("data", {}).get("result", [])
        if not data:
            return 0.0
        return float(data[0]["value"][1])
    except Exception:
        return 0.0

def collect_signals() -> dict:
    return {
        "p95_ttfb": prom_query('histogram_quantile(0.95,sum(rate(nginx_http_response_time_seconds_bucket[5m])) by (le))'),
        "rate_5xx": prom_query('sum(rate(nginx_http_requests_total{status=~"5.."}[5m]))'),
        "hit_ratio": prom_query('sum(rate(nginx_http_requests_total{cache="HIT"}[5m])) / ignoring(cache) sum(rate(nginx_http_requests_total[5m]))'),
        "p95_upstream_connect": prom_query('histogram_quantile(0.95,sum(rate(nginx_http_upstream_connect_time_seconds_bucket[5m])) by (le))'),
        "rate_404": prom_query('sum(rate(nginx_http_requests_total{status="404"}[5m]))')
    }

def heuristics(s: dict) -> list:
    hints = []
    if s.get("rate_5xx", 0) > 0.5:
        hints.append("ALTA_TASA_5XX")
    if s.get("p95_ttfb", 0) > 0.7 and s.get("hit_ratio", 1) < 0.4:
        hints.append("CACHE_BAJA_TTFB_ALTO")
    if s.get("rate_404", 0) > 0.3:
        hints.append("SEGMENT_404")
    if s.get("p95_upstream_connect", 0) > 0.3:
        hints.append("ORIGIN_LENTO")
    return hints

def retrieve_snippets(hints: list) -> list:
    kb = {
        "ALTA_TASA_5XX": "Revisar DNS/upstream. Agregar 'resolver <IP-CoreDNS>;' o upstream estático y 'proxy_pass http://origin_upstream;'",
        "CACHE_BAJA_TTFB_ALTO": "Verificar proxy_cache, proxy_cache_key, y headers Cache-Control del origin.",
        "SEGMENT_404": "Validar pipeline ffmpeg, rotación de .ts, consistencia con #EXTINF/playlist.",
        "ORIGIN_LENTO": "Chequear red/CPU origin, tc netem, tamaño de segmentos, upstream_keepalive."
    }
    return [kb[h] for h in hints if h in kb]

def llm_stub(signals: dict, hints: list, snippets: list) -> dict:
    # Sustituir por llamada real a Groq/HF/OpenAI si tenés clave
    return {
        "hypothesis": "Cache mal configurada y posible latencia en origin",
        "root_cause": "Falta de proxy_cache_key coherente y upstream sin resolver/estático",
        "checks": [
            'PromQL HIT%: sum(rate(nginx_http_requests_total{cache="HIT"}[5m]))/sum(rate(nginx_http_requests_total[5m]))',
            'grep -R "resolver\|upstream" /etc/nginx/nginx.conf',
            'kubectl exec deploy/origin -- tc qdisc show dev eth0'
        ],
        "remediation": [
            "Definir upstream estático: upstream origin_upstream { server origin-svc:80; } + proxy_pass http://origin_upstream;",
            "Configurar proxy_cache_path y proxy_cache_key $scheme$host$uri$is_args$args;",
            "Remover tc netem si está aplicado; reiniciar edge: kubectl rollout restart deploy/edge"
        ],
        "verification": [
            "HIT% > 0.7 en 5-10m",
            "p95 TTFB < 0.3s",
            "rate_5xx ≈ 0"
        ]
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/diagnose")
def diagnose():
    signals = collect_signals()
    hints = heuristics(signals)
    snippets = retrieve_snippets(hints)
    # En producción, reemplazar por LLM real
    diagnosis = llm_stub(signals, hints, snippets)
    return {"signals": signals, "hints": hints, "snippets": snippets, "diagnosis": diagnosis}
