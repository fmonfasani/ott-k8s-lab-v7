
    api-build:
        docker build -t yourrepo/ai-api:latest ./api
    api-run:
        uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload
    api-deploy-demo:
        kubectl apply -k k8s/api/overlays/demo
    api-deploy-dev:
        kubectl apply -k k8s/api/overlays/dev
