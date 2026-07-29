# Hello Docker

A minimal Docker image that starts a container, prints `Hello from Docker!`, and exits successfully.

## Check Docker

```bash
docker --version
sudo systemctl status docker --no-pager
```

## Build the image

```bash
cd "4 - 7 yrs/Docker/Hello Docker"
docker build -t hello-docker .
```

## Run the container

```bash
docker run --rm hello-docker
```

Expected output:

```text
Hello from Docker!
```

The `--rm` option removes the stopped container automatically after it prints the message.
