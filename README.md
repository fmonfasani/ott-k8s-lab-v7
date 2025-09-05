# OTT-K8s Lab v7 (mínimo viable)
- APIs: auth, catalog
- CDN edge (Nginx cache)
- Player HLS (hls.js)
- VLC streaming (HLS)
- Istio (Gateway + VirtualService)
Despliegue rápido:
kubectl apply -f k8s/00-namespace.yaml
istioctl install -y --set profile=demo
kubectl label ns ott-platform istio-injection=enabled --overwrite
kubectl apply -f k8s/apis/ -f k8s/cdn/ -f k8s/player/ -f k8s/vlc/ -f k8s/istio/
