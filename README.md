# OTT-K8s Lab v7

Plataforma OTT mínima para practicar despliegues Kubernetes "prod-like" con Istio, observabilidad y pruebas.

## Resumen
- APIs Python: auth, subscription, catalog, license (DRM), CAS.
- CDN edge Nginx con caché.
- Transcoder HLS estable (ffmpeg + nginx).
- Player HLS (hls.js) y pruebas k6.
- Prometheus + Grafana para métricas y dashboards.

## Requisitos
- Cluster Kubernetes local (**minikube** o **kind**).
- Herramientas: **kubectl**, **istioctl** v1.17+, **helm** 3.x.
- Opcional: stack de monitoreo tipo kube-prometheus-stack.

## Despliegue rápido
```bash
kubectl apply -f k8s/00-namespace.yaml
istioctl install -y --set profile=demo
kubectl label ns ott-platform istio-injection=enabled --overwrite
kubectl apply -f k8s/monitoring/
kubectl apply -f k8s/apis/ -f k8s/cdn/ -f k8s/vlc/ -f k8s/istio/
kubectl apply -f k8s/player/
kubectl apply -f k8s/testing/
kubectl logs -n ott-platform job/ott-load-test -f
```

## Acceso a Prometheus y Grafana
```bash
kubectl -n monitoring port-forward svc/prometheus-k8s 9090:9090
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

## Diagramas
```mermaid
flowchart LR
  A[HLS Player] --> B(CDN Nginx)
  B --> C(FFmpeg Transcoder)
  B --> D(Auth API)
  B --> E(Catalog API)
  B --> F(Subscription API)
  B --> G(License API DRM)
  B --> H(CAS API)
  K[Istio Ingress] --> B
  B --> I(Prometheus/Grafana)
  B --> J(k6 E2E)
```

```mermaid
sequenceDiagram
  participant P as Player
  participant GW as Istio Ingress
  participant A as Auth
  participant S as Subscription
  participant C as Catalog
  participant L as License
  participant CDN as CDN Nginx
  participant T as Transcoder
  P->>GW: Login
  GW->>A: /auth/login
  A-->>GW: token
  GW-->>P: token
  P->>GW: Catalog
  GW->>C: /catalog/content123
  C-->>GW: manifestUrl
  GW-->>P: manifestUrl
  P->>GW: License
  GW->>L: /license
  L-->>GW: licenseKey
  GW-->>P: licenseKey
  P->>CDN: GET master.m3u8
  CDN->>T: Fetch segments
  CDN-->>P: HLS stream
```

## k6 E2E
Ejecutá y revisá métricas:
```bash
kubectl logs -n ott-platform job/ott-load-test -f
```
