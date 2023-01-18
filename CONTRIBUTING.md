# CONTRIBUTING

## How to launch locally

```commandline
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run"
```

Uses local sqlite db for development purposes