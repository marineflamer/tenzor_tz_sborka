#!/bin/bash

# Получаем список нужных юнитов
units=$(systemctl list-units --type=service --all | grep -oP '^foobar-[^ ]+')

# Обработка каждого юнита
for unit in $units; do
    echo "Обработка юнита: $unit"

    # Получение пути к юнит-файлу
    unit_file=$(systemctl show -p FragmentPath "$unit" | cut -d= -f2)

    # Проверка существования юнит-файла
    if [[ ! -f "$unit_file" ]]; then
        echo "Не удалось найти юнит-файл для $unit, пропускаем."
        continue
    fi

    # Извлечение названия сервиса
    service_name=$(echo "$unit" | sed 's/^foobar-//')

    # Останов сервиса
    echo "Остановка $unit..."
    systemctl stop "$unit"

    # Перенос каталога
    src="/opt/misc/$service_name"
    dst="/srv/data/$service_name"

    if [[ -d "$src" ]]; then
        echo "Перемещение $src → $dst"
        mv "$src" "$dst"
    else
        echo "Каталог $src не найден, пропускаем $unit."
        continue
    fi

    # Обновление юнит-файла
    echo "Обновление юнит-файла $unit_file"
    sed -i "s|WorkingDirectory=/opt/misc/$service_name|WorkingDirectory=/srv/data/$service_name|" "$unit_file"
    sed -i "s|ExecStart=/opt/misc/$service_name/foobar-daemon|ExecStart=/srv/data/$service_name/foobar-daemon|" "$unit_file"

    # Перезагрузка systemd и запуск сервиса
    echo "Перезапуск systemd и запуск $unit"
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl start "$unit"

    echo "Юнит $unit обработан."
    echo "---------------------------"
done

echo "Все юниты обработаны."
