#!/bin/bash

IMAGE_NAME="cloud_tester:latest"

echo "Checking if image $IMAGE_NAME exists in the registry..."

if docker pull $IMAGE_NAME; then
    echo "Image $IMAGE_NAME exists in the registry. Pushing again..."
    docker push $IMAGE_NAME
else
    echo "Image $IMAGE_NAME does not exist in the registry. Pushing for the first time..."
    docker push $IMAGE_NAME
fi
