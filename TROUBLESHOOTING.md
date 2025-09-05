1) Caer License/DRM (cuando lo agregues) → alerta.
2) Limpiar caché CDN: restart deploy cdn-edge → ver X-Cache-Status.
3) VLC sin fuente: corregir hostPath en k8s/vlc/vlc-streaming.yaml.


### Notas finales
- **VLC**: editá el `hostPath` en `k8s/vlc/vlc-streaming.yaml` a tu carpeta local con un `.mp4`.
- Si usás **kube-prometheus-stack**, tus CRDs ya están; si no, aplica igual nuestros YAML (no rompen).
- Para correr el test E2E: `kubectl apply -f k8s/testing/ && kubectl logs -n ott-platform job/ott-load-test -f`.

¿Te queda bien así? Si querés, después te agrego **ArgoCD (GitOps)** en otra pasada.
