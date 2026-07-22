# Static Website Deployment — Stimulated Kubernetes Task

This simulated task demonstrates three common Kubernetes resources:

- A `ConfigMap` stores an HTML homepage.
- A `Deployment` runs two Nginx replicas.
- A `Service` provides one stable endpoint for the replicas.

## Deploy

```bash
cd "4 - 7 yrs/Kubernetes - Stimulated Task/Static Website Deployment"
kubectl apply -f kubernetes.yaml
kubectl rollout status deployment/skillmetrix-web --timeout=180s
```

## View in a browser

```bash
kubectl port-forward service/skillmetrix-web 8081:80
```

Open <http://localhost:8081>.

## Inspect

```bash
kubectl get deployment,pods,service -l app=skillmetrix-web
```

## Remove

```bash
kubectl delete -f kubernetes.yaml
```
