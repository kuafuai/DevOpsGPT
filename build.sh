#!/bin/bash

# Get the current commit SHA
COMMIT_SHA=$(git rev-parse HEAD)

# Get the current date in the format YYYYMMDD
CURRENT_DATE=$(date +%Y%m%d)

# Construct the new tag
NEW_TAG="${CURRENT_DATE}-${COMMIT_SHA:0:7}"

# Build the Docker image with the new tag
docker build -t "${DOCKER_REPO}:${NEW_TAG}" -t "${DOCKER_REPO}:latest" -f Dockerfile .

# Login to Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Push the Docker image with the new tag
docker push "${DOCKER_REPO}:${NEW_TAG}"
docker push "${DOCKER_REPO}:latest"