#!/bin/bash

#список юнитов
units=$(systemctl list-units --type=service --all | grep -oP '^foobar-[^ ]+')

for unit in $units; do
    echo "Обработка юнита: $unit"


    unit_file=$(systemctl show -p FragmentPath "$unit" | cut -d= -f2)


    if [[ ! -f "$unit_file" ]]; then
        echo "Не удалось найти юнит-файл для $unit, пропускаем."
        continue
    fi

    #названия сервиса
    service_name=$(echo "$unit" | sed 's/^foobar-//')
    echo "Остановка $unit..."
    systemctl stop "$unit"

    src="/opt/misc/$service_name"
    dst="/srv/data/$service_name"

    if [[ -d "$src" ]]; then
        echo "Перемещение $src → $dst"
        mv "$src" "$dst"
    else
        echo "Каталог $src не найден, пропускаем $unit."
        continue
    fi

    echo "Обновление юнит-файла $unit_file"
    sed -i "s|WorkingDirectory=/opt/misc/$service_name|WorkingDirectory=/srv/data/$service_name|" "$unit_file"
    sed -i "s|ExecStart=/opt/misc/$service_name/foobar-daemon|ExecStart=/srv/data/$service_name/foobar-daemon|" "$unit_file"
    echo "Перезапуск systemd и запуск $unit"
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl start "$unit"

    echo "Юнит $unit обработан."
    echo "---------------------------"
done

echo "Все юниты обработаны."
