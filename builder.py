import os
import sys
import shutil
import json
import subprocess
import datetime
from pathlib import Path

import argparse

def log(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}")

def clone_repo(repo_url, temp_dir):
    log(f"Клонирование репозитория: {repo_url}")
    subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
    log("Клонирование завершено")

def cleanup_repo(temp_dir, code_path):
    log("Удаление лишних директорий в корне репозитория")
    abs_code_path = os.path.join(temp_dir, code_path)
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path):
            os.remove(item_path)
    log("Очистка завершена")

def create_version_json(code_dir, version):
    log("Создание файла version.json")
    valid_extensions = (".py", ".js", ".sh")
    files = [f.name for f in Path(code_dir).iterdir() if f.suffix in valid_extensions and f.is_file()]
    
    data = {
        "name": "hello world ",
        "version": version,
        "files": files
    }

    version_path = os.path.join(code_dir, "version.json")
    with open(version_path, "w") as f:
        json.dump(data, f, indent=4)
    log(f"Файл version.json создан: {version_path}")
    return version_path

def create_archive(code_dir):
    log("Создание архива")
    archive_name = os.path.basename(code_dir.rstrip("/\\"))
    date_str = datetime.datetime.now().strftime("%d%m%Y")
    archive_filename = f"{archive_name}{date_str}.zip"
    
    shutil.make_archive(archive_name + date_str, 'zip', code_dir)
    log(f"Архив создан: {archive_filename}")
    return archive_filename

def main():
    parser = argparse.ArgumentParser(description="Сборочный скрипт")
    parser.add_argument("repo_url", help="URL репозитория")
    parser.add_argument("code_path", help="Относительный путь до исходного кода внутри репозитория")
    parser.add_argument("version", help="Версия продукта")

    args = parser.parse_args()

    temp_dir = "temp_repo"
    try:
        clone_repo(args.repo_url, temp_dir)
        cleanup_repo(temp_dir, args.code_path)

        full_code_path = os.path.join(temp_dir, args.code_path)
        version_file = create_version_json(full_code_path, args.version)
        archive_name = create_archive(full_code_path)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        log("Временные файлы удалены")
        
    except Exception as e:
        log(f"Ошибка: {e}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        log("Временные файлы удалены")

if __name__ == "__main__":
    main()
 