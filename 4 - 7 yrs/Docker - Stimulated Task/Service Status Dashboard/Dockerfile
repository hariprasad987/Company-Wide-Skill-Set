FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="Service Status Dashboard"
LABEL org.opencontainers.image.description="A stimulated Docker task serving a static operations dashboard"

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1/ || exit 1
