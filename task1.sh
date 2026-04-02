#!/bin/bash
# task1.sh

set -euo pipefail

echo "1. Замена имен:"
# Заменяем строки с именем и фамилией на "Имя: Аноним"
sed -E 's/^Имя: [[:upper:]][[:lower:]]+ [[:upper:]][[:lower:]]+$/Имя: Аноним/g' data.txt

echo -e "\n2. Удаление телефонов:"
# Удаляем все строки, содержащие телефонные номера
sed '/^Телефон:/d' data.txt

echo -e "\n3. Изменение формата email:"
# Заменяем символ @ на [at] только в строках Email
sed '/^Email:/ s/@/[at]/g' data.txt

echo -e "\n4. Только строки с Email:"
# Выводим только строки с Email
sed -n '/^Email:/p' data.txt
