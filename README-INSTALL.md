
# AI API Stub — OTT K8s Lab

## Cómo integrar
1) Copiá el contenido de este paquete dentro de tu repo `ott-k8s-lab` (no pisa nada).
2) Agregá `k8s/api/overlays/demo` (y/o `dev`) a tu `k8s/overlays/<env>/kustomization.yaml` global:
   ```yaml
   resources:
     - ../../api/overlays/demo
   ```
3) Build & run local:
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload
   ```
4) Docker:
   ```bash
   docker build -t yourrepo/ai-api:latest ./api
   docker run -p 8080:8080 -e PROM_URL=http://prometheus.monitoring:9090 yourrepo/ai-api:latest
   ```
5) Kubernetes (overlay demo):
   ```bash
   kubectl apply -k k8s/api/overlays/demo
   ```
6) Evaluación rápida:
   ```bash
   python api/eval/run_eval.py
   ```

## Endpoints
- `GET /health`
- `POST /diagnose`

Ajustá `PROM_URL` si tu Prometheus está en otra URL.
