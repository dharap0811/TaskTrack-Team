# TaskTrack Kubernetes Operations

## Check cluster

kubectl get nodes
kubectl get pods -n tasktrack
kubectl get deployments -n tasktrack
kubectl get services -n tasktrack

## Deploy application

The deployment uses a published Docker image from GitHub Container Registry (GHCR).

kubectl apply -f k8s/
kubectl rollout status deployment/redis -n tasktrack
kubectl rollout status deployment/tasktrack -n tasktrack

## Check application health

kubectl port-forward service/tasktrack-service 8000:80 -n tasktrack

Keep port forwarding running. In another PowerShell window:

Invoke-RestMethod http://localhost:8000/health

Expected result: healthy

## Scale to 3 replicas

kubectl scale deployment/tasktrack --replicas=3 -n tasktrack
kubectl rollout status deployment/tasktrack -n tasktrack
kubectl get pods -n tasktrack

## Rolling update

The rolling update was tested by changing an environment variable.

kubectl set env deployment/tasktrack APP_TITLE="TaskTrack Final Demo" -n tasktrack
kubectl rollout status deployment/tasktrack -n tasktrack
kubectl get pods -n tasktrack

## Rollback

kubectl rollout history deployment/tasktrack -n tasktrack
kubectl rollout undo deployment/tasktrack -n tasktrack
kubectl rollout status deployment/tasktrack -n tasktrack

Verify that APP_TITLE is restored to TaskTrack Team.

## Automatic pod recovery

List the running pods:

kubectl get pods -n tasktrack

Delete one TaskTrack pod using its actual name:

kubectl delete pod POD_NAME -n tasktrack

Verify Kubernetes creates a replacement:

kubectl rollout status deployment/tasktrack -n tasktrack
kubectl get pods -n tasktrack

## Troubleshooting

kubectl describe deployment tasktrack -n tasktrack
kubectl get events -n tasktrack --sort-by=.metadata.creationTimestamp
kubectl logs deployment/tasktrack -n tasktrack

## Access application

kubectl port-forward service/tasktrack-service 8000:80 -n tasktrack

Open http://localhost:8000

## Test results

The TaskTrack deployment was tested successfully on November 22, 2026.

Completed demonstrations:
- Application deployment and health checks
- Scaling from 2 to 3 replicas
- Automatic pod recovery
- Rolling update using an environment variable
- Rollback to the previous configuration

See docs/evidence/kubernetes-test-results.txt for details.

## Limitations

Redis uses temporary emptyDir storage in Kubernetes.
Data may be lost if the Redis pod is recreated.

The rolling update demonstration changed an environment variable,
not the Docker image version.
