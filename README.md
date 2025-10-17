# 🎮 OTT Streaming Platform on Kubernetes

### *Qualabs-ready Lab – Video Delivery, Observability & Automation*

---

## 📖 Descripción general

Este laboratorio implementa una **plataforma OTT completa en Kubernetes**, diseñada para demostrar dominio técnico en **video delivery distribuido, observabilidad, autoescalado y resiliencia**, alineado con las responsabilidades del rol **Video Streaming Engineer en Qualabs**.

Reproduce el flujo **end-to-end** de una solución de video profesional: desde el *transcoder* (ingesta de contenido) hasta el *player final* (reproducción), pasando por caché CDN, APIs OTT, malla de servicios segura (Istio) y monitoreo centralizado (Prometheus + Grafana + k6).

---

## 🧩 Arquitectura general

```
[User / Player]
      │
      ▼
 ┌────────────┐       ┌────────────┐
 │  Istio     │─────▶│ CDN Edge     │──▶ (Cache + TTL)
 └────────────┘       └────────────┘
                           │
                           ▼
                  ┌──────────────────────────┐
                  │ HLS Transcoder │───▶ .m3u8 + .ts segments
                  └──────────────────────────┘
                           │
                           ▼
          ┌──────────────────────────────────────────────┐
          │  OTT APIs: Auth, Catalog, CAS,  │
          │  License, Subscription          │
          └──────────────────────────────────────────────┘
                           │
                           ▼
          ┌──────────────────────────────────────────────┐
          │ Observability (Prometheus/Grafana) │
          │ + k6 Load Testing + HPA Scaling  │
          └──────────────────────────────────────────────┘
```

---

## ⚙️ Componentes principales

| Categoría                      | Descripción                                                                                                       | Archivos clave                                 |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **APIs OTT**                   | Microservicios que simulan backend de autenticación, catálogo, suscripción, licencias y CAS (Conditional Access). | `k8s/apis/*.yaml`                              |
| **Transcoder**                 | Servicio basado en *ffmpeg* que convierte videos en flujos HLS (.m3u8, .ts).                                      | `k8s/vlc/hls-transcoder.yaml`                  |
| **CDN Edge**                   | Proxy Nginx con caching, simula PoPs de Akamai/Fastly/CloudFront.                                                 | `k8s/cdn/cdn-edge.yaml`                        |
| **HLS Player**                 | Cliente web o VLC embebido que solicita segmentos y reproduce contenido.                                          | `k8s/player/hls-player.yaml`                   |
| **Malla de Servicios (Istio)** | Controla seguridad (mTLS), routing, balanceo, retries y failover.                                                 | `k8s/istio/*.yaml`                             |
| **Monitoreo & Alertas**        | Prometheus recolecta métricas y Grafana las visualiza (QoS/QoE).                                                  | `k8s/monitoring/*.yaml`                        |
| **Testing**                    | K6 simula usuarios y genera métricas end-to-end (startup time, rebuffer, error rate).                             | `k8s/testing/k6-configmap.yaml`, `k6-job.yaml` |
| **Autoescalado (HPA)**         | Escala automáticamente pods de APIs según carga.                                                                  | `k8s/apis/hpa.yaml`                            |
| **GitOps (ArgoCD)**            | Mantiene la configuración sincronizada con el repositorio (self-healing declarativo).                             | `gitops/argocd/app.yaml`                       |

---

## 🚀 Despliegue paso a paso

```bash
# 1️⃣ Crear el namespace base
kubectl apply -f k8s/00-namespace.yaml

# 2️⃣ Desplegar microservicios OTT
kubectl apply -f k8s/apis/

# 3️⃣ Desplegar CDN y Transcoder
kubectl apply -f k8s/cdn/cdn-edge.yaml
kubectl apply -f k8s/vlc/hls-transcoder.yaml

# 4️⃣ Desplegar Player HLS
kubectl apply -f k8s/player/hls-player.yaml

# 5️⃣ Configurar Istio (Gateway, VirtualServices, Security)
kubectl apply -f k8s/istio/

# 6️⃣ Desplegar Observabilidad (Prometheus + Grafana)
kubectl apply -f k8s/monitoring/

# 7️⃣ Ejecutar pruebas E2E (k6)
kubectl apply -f k8s/testing/k6-configmap.yaml
kubectl apply -f k8s/testing/k6-job.yaml

# 8️⃣ Activar GitOps con ArgoCD (opcional)
kubectl apply -f gitops/argocd/app.yaml
```

---

## 📊 Observabilidad y métricas

### Métricas recolectadas

* **QoS:** latencia promedio, tasa de errores HTTP, throughput.
* **QoE:** startup time, rebuffer ratio, bitrate efectivo (a integrar).
* **Sistema:** uso de CPU, memoria, requests por segundo.
* **Infraestructura:** estado de pods, tiempo de respuesta por API.

### Dashboards principales

* `grafana-dashboard-configmap.yaml` contiene los paneles base.
* Se pueden extender para QoE (bitrate, buffering, QoS per CDN).

### Alertas Prometheus

* Definidas en `prometheus-rules.yaml`.
  Ejemplo:

  ```yaml
  - alert: StreamLatencyHigh
    expr: avg(stream_segment_latency_seconds) > 3
    for: 2m
    labels:
      severity: warning
  ```

---

## 🧠 Pruebas automatizadas (K6)

Los scripts en `k6-configmap.yaml` simulan usuarios reales:

* Login → acceso al catálogo → reproducción HLS.
* Métricas generadas: `video_start_time`, `segment_download_time`, `buffer_events`.

Se ejecutan como Job (`k6-job.yaml`) y los resultados se integran en Prometheus.

---

## 🧬 Capacidades demostradas (alineadas al puesto Qualabs)

| Competencia                         | Evidencia en el laboratorio                                    |
| ----------------------------------- | -------------------------------------------------------------- |
| CDN operations & video delivery     | `cdn-edge.yaml`, simulación de PoPs, control de TTL y caching. |
| Distributed systems troubleshooting | Istio + Prometheus + Grafana integrados con k6.                |
| Self-healing systems                | HPA + GitOps con ArgoCD y sincronización automática.           |
| Observabilidad                      | Métricas QoS/QoE y dashboards correlacionados.                 |
| Python scripting / IaC              | Automatización y manifiestos declarativos (K8s + Argo).        |
| Incident response & playbooks       | `TROUBLESHOOTING.md` y alertas Prometheus integradas.          |

---

## 🧩 Próximas mejoras (para nivel production-grade)

* Integración con **CDNs comerciales (Akamai, Fastly, CloudFront)**.
* Dashboards QoE enriquecidos (bitrate, rebuffer, ABR).
* **Auto-remediación basada en alertas** (reinicios automáticos, failover).
* Módulo de **simulación multi-región / multi-CDN**.
* **Terraform + Helm** para infraestructura reproducible.

---

## 🗾 Créditos

**Autor:** Federico Monfasani
**Rol:** Telecom Engineer & Software Developer
**Objetivo:** Demostrar experiencia integral en arquitectura OTT, observabilidad y delivery de video distribuido, aplicable al puesto de *Video Streaming Engineer en Qualabs*.
