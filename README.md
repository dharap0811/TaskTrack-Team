# TaskTrack-Team

A personal task tracker application developed for the IT 390 Introduction to Containers final team project at DePaul University.

The project uses FastAPI, Redis, Docker, GitHub Actions, GitHub Container Registry (GHCR), and Kubernetes.

## Project Overview

TaskTrack is a simple task management application that allows users to create, view, and complete tasks.

The goal of this project was to build a containerized application and demonstrate how it can be tested, deployed, managed, and recovered using modern DevOps tools.

## Technologies Used

- Python and FastAPI - application backend
- Redis - task data storage
- Docker - application containerization
- Docker Compose - local multi-container deployment
- GitHub Actions - automated CI/CD pipeline
- GHCR - Docker image registry
- Kubernetes - application deployment and management
- kind - local Kubernetes cluster

## Application Features

The application supports:

- Creating tasks
- Viewing tasks
- Marking tasks as complete
- Checking application health

API endpoints:

- GET /
- GET /health
- POST /tasks
- GET /tasks
- PATCH /tasks/{id}/complete

## Run Locally with Docker Compose

Requirements:

- Docker Desktop
- Docker Compose

Clone the repository:

git clone https://github.com/dharap0811/TaskTrack-Team.git

Enter the project directory:

cd TaskTrack-Team

Start the application:

docker compose up --build -d

Open:

http://localhost:8000

Check application health:

http://localhost:8000/health

Stop the application:

docker compose down

## CI/CD Pipeline

The GitHub Actions workflow is located at:

.github/workflows/ci.yml

The pipeline runs when code is pushed to main or a pull request targets main.

It performs three main jobs:

1. Validates project configuration files.
2. Runs automated FastAPI tests.
3. Builds and publishes the Docker image to GHCR after successful checks on main.

Published Docker image:

ghcr.io/dharap0811/tasktrack-team:sha-467f8e248c9ebb04ff7382a8f1a56c5ceb229d1d

## Kubernetes Deployment

Requirements:

- Docker Desktop
- kubectl
- kind

Create the Kubernetes cluster:

kind create cluster --name tasktrack

Create the namespace:

kubectl create namespace tasktrack

Deploy the application and Redis:

kubectl apply -f k8s/

Check the deployment:

kubectl get pods -n tasktrack
kubectl get services -n tasktrack

Wait for the application:

kubectl rollout status deployment/tasktrack -n tasktrack

Access TaskTrack:

kubectl port-forward service/tasktrack-service 8000:80 -n tasktrack

Open:

http://localhost:8000

## Kubernetes Demonstrations

The following tests were successfully completed using the actual TaskTrack application:

1. Application deployment and health checks
2. Scaling from 2 to 3 replicas
3. Automatic pod replacement
4. Rolling update using an environment variable
5. Rollback to the previous configuration

Example scaling command:

kubectl scale deployment/tasktrack --replicas=3 -n tasktrack

Example rolling update:

kubectl set env deployment/tasktrack APP_TITLE="TaskTrack Final Demo" -n tasktrack

Example rollback:

kubectl rollout undo deployment/tasktrack -n tasktrack

Detailed instructions are available in:

docs/kubernetes-operations.md

Test evidence is available in:

docs/evidence/kubernetes-test-results.txt

## Testing

Automated application tests are located in the tests directory.

Run the tests locally after installing development dependencies:

pip install -r requirements-dev.txt

pytest -v

The CI/CD pipeline also runs these tests automatically.

## Project Limitations

The Kubernetes Redis deployment currently uses temporary storage. Task data may be lost if the Redis pod is recreated.

The rolling update demonstration used an environment variable change rather than a new Docker image version.

## Team Contributions

Both team members contributed to developing and testing the final application.

Main areas of responsibility:

- Application development, Dockerfile, Docker Compose, and automated tests
- GitHub Actions CI/CD, GHCR publishing, Kubernetes deployment, and operational testing

## Documentation

- Kubernetes operations: docs/kubernetes-operations.md
- Kubernetes test evidence: docs/evidence/kubernetes-test-results.txt
