1) License/DRM caído → verificar pods:
```bash
kubectl get pods -n ott-platform -l app=license
```

2) Cache MISS en CDN → inspeccionar encabezados:
```bash
kubectl -n ott-platform exec deploy/cdn-edge -- curl -I http://cdn-edge/manifest.m3u8
```

3) Limpiar caché CDN → reiniciar despliegue:
```bash
kubectl -n ott-platform rollout restart deployment/cdn-edge
```

4) Ruta de video incorrecta → revisar VirtualService:
```bash
kubectl -n ott-platform get virtualservice player-vs -o yaml
```

5) Latencia elevada en Istio → ver métricas del sidecar:
```bash
kubectl -n ott-platform exec deploy/auth -c istio-proxy -- curl -sS localhost:15000/stats | grep upstream_rq_time
```

6) Circuit breaker activado → inspeccionar DestinationRule:
```bash
kubectl -n ott-platform describe destinationrule license-dr
```

7) Pod en CrashLoopBackOff → eventos y logs:
```bash
kubectl -n ott-platform describe pod <pod>
kubectl -n ott-platform logs <pod> -c <container>
```

8) ConfigMap sin aplicar → reiniciar despliegue:
```bash
kubectl -n ott-platform rollout restart deployment/auth
```

9) Job k6 fallando → revisar logs:
```bash
kubectl logs -n ott-platform job/ott-load-test
```

10) Grafana inaccesible → reenviar puerto:
```bash
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

