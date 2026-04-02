#!/bin/bash
# task3.sh

set -euo pipefail

echo "1. Только ERROR сообщения:"
# Извлекаем только сообщения уровня ERROR
sed -En '/ERROR:/p' server.log

echo -e "\n2. Логи без временных меток:"
# Удаляем временную метку вида [YYYY-MM-DD HH:MM:SS]
sed -E 's/^\[[0-9-]+ [0-9:]+\] //' server.log

echo -e "\n3. Замена уровней логирования:"
# Заменяем INFO->ℹ, WARNING->!, ERROR->!!
sed -E 's/\bINFO:\b/ℹ:/g; s/\bWARNING:\b/!:/g; s/\bERROR:\b/!!:/g' server.log

echo -e "\n4. Все IP-адреса в логах:"
# Ищем и выводим IPv4-адреса из логов
sed -En 's/.*\b(([0-9]{1,3}\.){3}[0-9]{1,3})\b.*/\1/p' server.log

echo -e "\n5. Удаление лишних пробелов:"
# Удаляем повторяющиеся пробелы и пробелы по краям строки
sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//' server.log
