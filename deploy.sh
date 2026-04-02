#!/bin/bash
# deploy.sh

set -euo pipefail

required_vars=(
  DB_HOST DB_PORT DB_NAME DB_USER DB_PASS
  SERVER_PORT DEBUG_MODE LOG_LEVEL
)

for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo "Ошибка: переменная окружения $var не задана" >&2
    exit 1
  fi
done

sed -E \
  -e "s#^host = .*#host = ${DB_HOST}#" \
  -e "s#^port = 3306#port = ${DB_PORT}#" \
  -e "s#^name = .*#name = ${DB_NAME}#" \
  -e "s#^user = .*#user = ${DB_USER}#" \
  -e "s#^password = .*#password = ${DB_PASS}#" \
  -e "s#^port = 8080#port = ${SERVER_PORT}#" \
  -e "s#^debug = .*#debug = ${DEBUG_MODE}#" \
  -e "s#^log_level = .*#log_level = ${LOG_LEVEL}#" \
  app.conf.template > app.conf

# Базовая проверка синтаксиса INI-конфига
if ! grep -qE '^\[Database\]$' app.conf || ! grep -qE '^\[Server\]$' app.conf; then
  echo "Ошибка: отсутствуют обязательные секции [Database] или [Server]" >&2
  exit 1
fi

for key in 'host = ' 'port = ' 'name = ' 'user = ' 'password = ' 'debug = ' 'log_level = '; do
  if ! grep -q "$key" app.conf; then
    echo "Ошибка: отсутствует ключ конфигурации: $key" >&2
    exit 1
  fi
done

echo "Конфиг app.conf успешно создан и проверен."
