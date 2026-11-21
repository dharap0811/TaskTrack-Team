# TaskTrack Kubernetes Operations

## Check cluster
kubectl get nodes
kubectl get pods -n tasktrack
kubectl get deployments -n tasktrack
kubectl get services -n tasktrack

## Deploy application
# Only after a real Docker image is published
kubectl apply -f k8s/
kubectl rollout status deployment/tasktrack -n tasktrack

## Scale to 3 replicas
kubectl scale deployment/tasktrack --replicas=3 -n tasktrack
kubectl get pods -n tasktrack

## Rolling update
# Replace IMAGE_TAG with a real published tag
kubectl set image deployment/tasktrack tasktrack=ghcr.io/dharap0811/tasktrack-team:IMAGE_TAG -n tasktrack
kubectl rollout status deployment/tasktrack -n tasktrack

## Rollback
kubectl rollout history deployment/tasktrack -n tasktrack
kubectl rollout undo deployment/tasktrack -n tasktrack

## Pod recovery
# Replace POD_NAME with an actual pod name
kubectl get pods -n tasktrack
kubectl delete pod POD_NAME -n tasktrack
kubectl get pods -n tasktrack

## Troubleshooting
kubectl describe deployment tasktrack -n tasktrack
kubectl get events -n tasktrack --sort-by=.metadata.creationTimestamp
kubectl logs deployment/tasktrack -n tasktrack

## Access application
kubectl port-forward service/tasktrack-service 8080:80 -n tasktrack

## Notes
The deployment requires a real GHCR image before testing.
Rolling updates and rollbacks require working image versions.
