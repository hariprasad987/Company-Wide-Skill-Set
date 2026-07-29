# Service Status Dashboard — Stimulated Docker Task

This project packages a responsive service-status webpage in an Nginx container. The image includes a Docker health check that requests the page every ten seconds.

## Build

```bash
cd "4 - 7 yrs/Docker - Stimulated Task/Service Status Dashboard"
docker build -t service-status-dashboard .
```

## Run

```bash
docker run --detach \
  --name service-status-dashboard \
  --publish 8082:80 \
  service-status-dashboard
```

Open <http://localhost:8082> in a browser.

## Verify

```bash
curl http://localhost:8082
docker ps --filter name=service-status-dashboard
docker inspect --format='{{.State.Health.Status}}' service-status-dashboard
```

## Stop and remove

```bash
docker stop service-status-dashboard
docker rm service-status-dashboard
```
