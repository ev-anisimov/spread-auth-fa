#!/bin/bash

set -eax

mkdir -p /configs/spread
ln -s /configs/spread /etc/ || true

# копируем настройки по-умолчанию, если файла настроек нет
cp -n /config/default.json "/etc/spread/${HOSTNAME}.json"
#cp /config/schema.json "/opt/schemas/${HOSTNAME}.schema.json"

sed "s/\${HOSTNAME}/$HOSTNAME/g" /snippets/location.snippet > "/etc/nginx/snippets/$HOSTNAME.location.snippet"
sed "s/\${HOSTNAME}/$HOSTNAME/g" /snippets/upstream.snippet > "/etc/nginx/snippets/$HOSTNAME.upstream.snippet"

rm "/awada-sockets/${HOSTNAME}.sock" || true
/application/.venv/bin/uvicorn \
    spread_auth.main:app \
    --timeout-keep-alive 300 \
    --uds "/opt/awada-sockets/${HOSTNAME}.sock"
