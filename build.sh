#!/bin/bash
#
# -- Build iFood MLOps app locally

# ----------------------------------------------------------------------------------------------------------------------
# -- Variables ---------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

BUILD_DATE="$(date -u +'%Y-%m-%d')"

# ----------------------------------------------------------------------------------------------------------------------
# -- Functions----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

function cleanContainers() {

    container="$(docker ps -a | grep 'serving' | awk '{print $1}')"
    docker stop "${container}"
    docker rm "${container}"

    container="$(docker ps -a | grep 'pipeline' | awk '{print $1}')"
    docker stop "${container}"
    docker rm "${container}"

    container="$(docker ps -a | grep 'sandbox' | awk '{print $1}')"
    docker stop "${container}"
    docker rm "${container}"

    container="$(docker ps -a | grep 'database' | awk '{print $1}')"
    docker stop "${container}"
    docker rm "${container}"

}

function cleanImages() {

  docker rmi -f "$(docker images | grep -m 1 'serving' | awk '{print $3}')"
  docker rmi -f "$(docker images | grep -m 1 'pipeline' | awk '{print $3}')"
  docker rmi -f "$(docker images | grep -m 1 'sandbox' | awk '{print $3}')"
  docker rmi -f "$(docker images | grep -m 1 'base' | awk '{print $3}')"

}

function cleanVolume() {
  docker volume rm "registry"
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

  docker build \
    --build-arg build_date="${BUILD_DATE}" \
    -f pipeline/Dockerfile \
    -t pipeline:latest .

  docker build \
    --build-arg build_date="${BUILD_DATE}" \
    -f serving/Dockerfile \
    -t serving:latest .

}

# ----------------------------------------------------------------------------------------------------------------------
# -- Main --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

cleanContainers;
cleanImages;
cleanVolume;
buildImages;