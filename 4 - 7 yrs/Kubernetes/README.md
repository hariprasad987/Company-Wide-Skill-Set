# Kubernetes Hello Pod

This task creates a Pod containing a BusyBox container that prints:

```text
Hello from Kubernetes!
```

## Run

With access to a Kubernetes cluster and `kubectl` configured:

```bash
cd "4 - 7 yrs/Kubernetes"
kubectl apply -f hello-pod.yaml
kubectl wait --for=jsonpath='{.status.phase}'=Succeeded pod/hello-kubernetes --timeout=120s
kubectl logs hello-kubernetes
```

To run the task again:

```bash
kubectl delete -f hello-pod.yaml --ignore-not-found
kubectl apply -f hello-pod.yaml
```
