#!/bin/bash
#
# -- Build iFood MLOps app locally

# ----------------------------------------------------------------------------------------------------------------------
# -- Variables ---------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

BUILD_DATE="$(date -u +'%Y-%m-%d')"

JUPYTERLAB_VERSION="3.0.0"

# ----------------------------------------------------------------------------------------------------------------------
# -- Functions----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

function cleanContainers() {

    container="$(docker ps -a | grep 'sandbox' | awk '{print $1}')"
    docker stop "${container}"
    docker rm "${container}"

    container="$(docker ps -a | grep 'database' | awk '{print $1}')"
    docker stop "${container}"
    docker rm "${container}"

}

function cleanImages() {

  docker rmi -f "$(docker images | grep -m 1 'sandbox' | awk '{print $3}')"
  docker rmi -f "$(docker images | grep -m 1 'database' | awk '{print $3}')"
  docker rmi -f "$(docker images | grep -m 1 'base' | awk '{print $3}')"

}

function cleanVolume() {
  docker volume rm "sandbox"
  docker volume rm "database"
}

function buildImages() {

  docker build \
    -f shared/Dockerfile \
    -t base:latest .

  docker build \
    --build-arg build_date="${BUILD_DATE}" \
    --build-arg jupyterlab_version="${JUPYTERLAB_VERSION}" \
    -f sandbox/Dockerfile \
    -t sandbox:latest .

}

# ----------------------------------------------------------------------------------------------------------------------
# -- Main --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

cleanContainers;
cleanImages;
cleanVolume;
buildImages;