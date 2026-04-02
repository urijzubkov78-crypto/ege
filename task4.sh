#!/bin/bash
# task4.sh

set -euo pipefail

text_cleanup() {
    local file=${1:?"Укажите входной файл"}

    sed -E '
        /^$/d
        s/.*/\L&/
        s/[[:punct:]]//g
    ' "$file"
}

echo "1. Текст после очистки:"
# Удаляем пустые строки, переводим в нижний регистр, убираем пунктуацию
text_cleanup text.txt

echo -e "\n2. Разбивка на слова (по одному в строке):"
# Разбиваем текст на отдельные слова
text_cleanup text.txt | sed -E 's/[[:space:]]+/\n/g' | sed '/^$/d'

echo -e "\n3. Частота слов (по убыванию):"
# Считаем частоту слов с сортировкой по убыванию
text_cleanup text.txt \
  | sed -E 's/[[:space:]]+/\n/g' \
  | sed '/^$/d' \
  | sort \
  | uniq -c \
  | sort -nr
