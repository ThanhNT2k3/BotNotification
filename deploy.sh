#!/bin/bash

# Configuration
RESOURCE_GROUP="TradingBotGroup"
LOCATION="southeastasia"
# Generate a unique registry name (must be alphanumeric)
REGISTRY_NAME="tradingbot$(date +%s)"
IMAGE_NAME="trading-bot:v1"
CONTAINER_NAME="trading-bot-container"

echo "Checking for Azure CLI..."
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI (az) is not installed. Please install it first."
    echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

echo "✅ Azure CLI found."
echo "Please login to Azure if you haven't already..."
az login --output none

echo "Creating Resource Group: $RESOURCE_GROUP..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "Creating Azure Container Registry: $REGISTRY_NAME..."
az acr create --resource-group $RESOURCE_GROUP --name $REGISTRY_NAME --sku Basic --admin-enabled true

echo "Logging into ACR..."
az acr login --name $REGISTRY_NAME

echo "Getting ACR Login Server..."
ACR_SERVER=$(az acr show --name $REGISTRY_NAME --query loginServer --output tsv)
echo "ACR Server: $ACR_SERVER"

echo "Building Docker Image..."
docker build -t $ACR_SERVER/$IMAGE_NAME .

echo "Pushing Docker Image to ACR..."
docker push $ACR_SERVER/$IMAGE_NAME

echo "Getting ACR Credentials..."
ACR_PASSWORD=$(az acr credential show --name $REGISTRY_NAME --query "passwords[0].value" --output tsv)

echo "Deploying to Azure Container Instances..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $ACR_SERVER/$IMAGE_NAME \
  --cpu 1 \
  --memory 1 \
  --registry-login-server $ACR_SERVER \
  --registry-username $REGISTRY_NAME \
  --registry-password $ACR_PASSWORD \
  --location $LOCATION \
  --restart-policy Always \
  --environment-variables TZ="Asia/Ho_Chi_Minh"

echo "✅ Deployment Complete!"
echo "You can check logs with: az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME"
