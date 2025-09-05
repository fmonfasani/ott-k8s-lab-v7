# Troubleshooting OTT Lab

1. **DRM/License API caído**
   ```bash
   kubectl get pods -n ott-platform -l app=license-api
   ```
2. **Cache MISS en CDN**
   ```bash
   kubectl -n ott-platform exec deploy/cdn-edge -- curl -I http://cdn-edge-service/media/demo/master.m3u8
   ```
3. **Limpiar caché del CDN**
   ```bash
   kubectl -n ott-platform rollout restart deployment/cdn-edge
   ```
4. **Ruta de video incorrecta**
   ```bash
   kubectl -n ott-platform get virtualservice api-routes -o yaml | grep -A1 cdn
   ```
5. **Latencia elevada en Istio**
   ```bash
   kubectl -n ott-platform exec deploy/auth-api-deployment -c istio-proxy -- curl -s localhost:15000/stats | grep upstream_rq_time
   ```
6. **DRM devuelve error**
   ```bash
   kubectl logs -n ott-platform deploy/license-api-deployment
   ```
7. **Pod en CrashLoopBackOff**
   ```bash
   kubectl -n ott-platform describe pod <pod>
   kubectl -n ott-platform logs <pod> -c <container>
   ```
8. **ConfigMap no aplicado**
   ```bash
   kubectl -n ott-platform rollout restart deployment/auth-api-deployment
   ```
9. **Job k6 fallando**
   ```bash
   kubectl logs -n ott-platform job/ott-load-test
   ```
10. **Grafana/Prometheus inaccesibles**
    ```bash
    kubectl -n monitoring port-forward svc/grafana 3000:3000
    kubectl -n monitoring port-forward svc/prometheus-k8s 9090:9090
    ```
