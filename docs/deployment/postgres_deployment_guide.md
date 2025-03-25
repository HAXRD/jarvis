# PostgreSQL Deployment Guide for LLM Chat Platform

This document outlines the steps to build, push, and deploy the PostgreSQL service for the LLM chat platform using Docker and Kubernetes with Minikube.

## Prerequisites

- Docker installed and running
- Minikube installed and configured
- kubectl installed and configured
- DataGrip or any PostgreSQL client for database connection

## Step 1: Building and Pushing the Docker Image

1. Navigate to your project root:
   ```bash
   cd /path/to/your/project
   ```

2. Build the PostgreSQL Docker image:
   ```bash
   docker build -t haxrd/postgres:latest -f deployment/docker/postgres.Dockerfile .
   ```

3. Push the image to your registry:
   ```bash
   docker push haxrd/postgres:latest
   ```

## Step 2: Starting Minikube and Deploying PostgreSQL

1. Start Minikube if it's not already running:
   ```bash
   minikube start
   ```

2. Apply the PostgreSQL Kubernetes configuration:
   ```bash
   kubectl apply -f deployment/kubernetes/postgres.yaml
   ```

3. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get pvc
   ```

4. Wait until the PostgreSQL pod is running:
   ```bash
   kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s
   ```

## Step 3: Accessing PostgreSQL from Outside the Cluster

### Option 1: Port Forwarding (Recommended for Development)

1. Forward local port 5432 to the PostgreSQL service:
   ```bash
   kubectl port-forward svc/postgres 5432:5432
   ```

### Option 2: Using Minikube Service

1. Get the URL for the PostgreSQL service:
   ```bash
   minikube service postgres --url
   ```

## Step 4: Connecting with DataGrip

1. Open DataGrip.
2. Click "New" > "Data Source" > "PostgreSQL".
3. Enter the following information:
   - **Host**: `localhost` (if using port forwarding) or the IP from Option 2
   - **Port**: `5432`
   - **Database**: `llmchat_db`
   - **Username**: `llmchat`
   - **Password**: `postgres_password`
4. Test the connection and click "Apply" and "OK".

## Step 5: Useful Commands for Management

- Check PostgreSQL logs:
  ```bash
  kubectl logs -l app=postgres
  ```

- Describe the PostgreSQL pod for more details:
  ```bash
  kubectl describe pod -l app=postgres
  ```

- Exec into the PostgreSQL pod for direct access:
  ```bash
  kubectl exec -it $(kubectl get pod -l app=postgres -o jsonpath="{.items[0].metadata.name}") -- psql -U llmchat -d llmchat_db
  ```

- Scale the PostgreSQL deployment (for testing only, not recommended for production):
  ```bash
  kubectl scale deployment postgres --replicas=1
  ```

- Delete the PostgreSQL deployment when needed:
  ```bash
  kubectl delete -f deployment/kubernetes/postgres.yaml
  ```
