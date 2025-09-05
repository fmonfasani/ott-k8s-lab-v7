# OTT-K8s Lab v7 (mínimo viable)
- APIs: auth, catalog
- CDN edge (Nginx cache)
- Player HLS (hls.js)
- VLC streaming (HLS)
- Istio (Gateway + VirtualService)

## Requisitos
- Cluster Kubernetes local con **minikube** o **kind**.
- **kubectl** configurado contra el cluster.
- **istioctl** v1.17+.
- **helm** 3.x.

## Extensiones incluidas
- APIs: **subscription**, **license (DRM)**, **CAS**.
- **k6** E2E (Auth → Sub → Catalog → DRM → Manifest).
- Observabilidad: **ServiceMonitors**, **PrometheusRule**, **Grafana** dashboard.
- Istio: **DestinationRules** y **mTLS** + **AuthorizationPolicy** (POST /license).

### Despliegue rápido
```bash
kubectl apply -f k8s/00-namespace.yaml
istioctl install -y --set profile=demo
kubectl label ns ott-platform istio-injection=enabled --overwrite
# (Si usás kube-prometheus-stack, mantenelo; si no, aplica nuestros objetos)
kubectl apply -f k8s/monitoring/
kubectl apply -f k8s/apis/ -f k8s/cdn/ -f k8s/player/ -f k8s/vlc/ -f k8s/istio/
kubectl apply -f k8s/testing/
kubectl logs -n ott-platform job/ott-load-test -f
```

### Exponer istio-ingressgateway
Minikube:
```bash
minikube tunnel &
kubectl -n istio-system get svc istio-ingressgateway
```
Kind u otros entornos sin LoadBalancer:
```bash
kubectl -n istio-system port-forward svc/istio-ingressgateway 8080:80
```

### Ejecutar Job k6
```bash
kubectl apply -f k8s/testing/
kubectl logs -n ott-platform job/ott-load-test -f
```

### Acceso a Grafana
```bash
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

