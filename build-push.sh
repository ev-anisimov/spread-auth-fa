#!/bin/bash
set -eax

# shellcheck disable=SC1091
. .env

case $1 in

"dev"|'')
    target="dev"
    platform="linux/amd64,linux/arm64"
    tags="  -t alpha.awada.systems/${IMAGE_NAME}:dev \
            --push"
    ;;

"build-local")
    target="dev"
    VERSION="local"
    platform="linux/amd64"
    tags="  -t alpha.awada.systems/${IMAGE_NAME}:local \
            -o type=docker"
    ;;

"run-local")
    VERSION="local"
    envsubst < compose.yaml | docker exec -i store cp /dev/stdin "/opt/awada/${SERVICE_NAME}.compose.yaml"
    docker exec -d \
        store \
        bash -c " \
            cp /opt/awada/${SERVICE_NAME}.compose.yaml /opt/awada/configurations/${SERVICE_NAME}.compose.override.yaml; \
            /opt/awada-cgi/products/activate.sh ${IMAGE_NAME} local; \
            /opt/awada-cgi/services/configurate.sh --silent;
        "
    exit 0
    ;;
*)
    target="production"
    platform="linux/amd64,linux/arm64"
    VERSION=$1
    tags="  -t alpha.awada.systems/${IMAGE_NAME}:$1 \
            -t alpha.awada.systems/${IMAGE_NAME}:latest \
            --push"
    ;;
esac

# shellcheck disable=SC2016
ENCODED_COMPOSE=$( envsubst '$IMAGE_NAME' < compose.yaml | base64 -w 0 )

# shellcheck disable=SC2086
docker buildx build \
    --platform "${platform}" \
    --target $target \
    ${tags} \
    --label VERSION="${VERSION}" \
    --label SYSTEM_REQUIRED="${SYSTEM_REQUIRED}" \
    --label SERVICE_NAME="${SERVICE_NAME}" \
    --label DESCRIPTION="${DESCRIPTION}" \
    --label DEPENDENCIES="${DEPENDENCIES}" \
    --label REPLICABLE="${REPLICABLE}" \
    --label ENCODED_COMPOSE="${ENCODED_COMPOSE}" \
    --build-arg DEV_REGISTRY="${DEV_REGISTRY}" \
    --build-arg PYTHON_VERSION="${PYTHON_VERSION}" \
    --build-arg NODE_VERSION="${NODE_VERSION}" \
    --pull \
    .
