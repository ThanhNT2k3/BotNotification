---
description: Deploy Trading Bot to Azure Container Instances (ACI)
---

This workflow guides you through deploying your Python trading bot to Azure using Docker and Azure Container Instances.

## Prerequisites
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) installed and logged in (`az login`).
- [Docker](https://docs.docker.com/get-docker/) installed and running.

## Steps

### 1. Create a Resource Group
Create a resource group to hold your resources.
```bash
az group create --name TradingBotGroup --location southeastasia
```

### 2. Create an Azure Container Registry (ACR)
Create a registry to store your Docker images. Replace `<registry_name>` with a unique name (e.g., `thanhnguyentrading`).
```bash
az acr create --resource-group TradingBotGroup --name <registry_name> --sku Basic
```

### 3. Log in to ACR
```bash
az acr login --name <registry_name>
```

### 4. Build and Push Docker Image
Build the image locally and push it to your ACR.
```bash
# Get the login server address
acrServer=$(az acr show --name <registry_name> --query loginServer --output tsv)

# Build the image
docker build -t $acrServer/trading-bot:v1 .

# Push the image
docker push $acrServer/trading-bot:v1
```

### 5. Deploy to Azure Container Instances (ACI)
Run the container in the cloud.
```bash
# Enable admin user on ACR to allow ACI to pull the image (simplest method for personal use)
az acr update -n <registry_name> --admin-enabled true

# Get the registry password
acrPassword=$(az acr credential show --name <registry_name> --query "passwords[0].value" --output tsv)

# Deploy container
az container create \
  --resource-group TradingBotGroup \
  --name trading-bot-container \
  --image $acrServer/trading-bot:v1 \
  --cpu 1 \
  --memory 1 \
  --registry-login-server $acrServer \
  --registry-username <registry_name> \
  --registry-password $acrPassword \
  --location southeastasia \
  --restart-policy Always
```

### 6. Verify Deployment
Check the logs to see if the bot is running.
```bash
az container logs --resource-group TradingBotGroup --name trading-bot-container
```

## Updating the Bot
If you change the code:
1. Rebuild the image: `docker build -t $acrServer/trading-bot:v2 .`
2. Push the image: `docker push $acrServer/trading-bot:v2`
3. Update the container:
   ```bash
   az container create \
     --resource-group TradingBotGroup \
     --name trading-bot-container \
     --image $acrServer/trading-bot:v2 \
     --cpu 1 \
     --memory 1 \
     --registry-login-server $acrServer \
     --registry-username <registry_name> \
     --registry-password $acrPassword \
     --location southeastasia \
     --restart-policy Always
   ```
