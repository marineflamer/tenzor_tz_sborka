import json
import argparse

def parse_version(version_str):
    return list(map(int, version_str.strip().split(".")))

def version_to_str(version_list):
    return ".".join(map(str, version_list))

def generate_versions_from_template(template):
    parts = template.split(".")
    versions = []
    for value in [1, 2, 3, 4, 5]:
        generated = []
        for part in parts:
            if part == "*":
                generated.append(value)
            else:
                generated.append(int(part))
        versions.append(generated)
    
    return versions

def compare_versions(v1, v2):
    len_diff = len(v1) - len(v2)
    if len_diff > 0:
        v2 += [0] * len_diff
    elif len_diff < 0:
        v1 += [0] * (-len_diff)
    return v1 < v2

def main():
    parser = argparse.ArgumentParser(description="Генератор версий по шаблонам")
    parser.add_argument("version", help="Базовая версия продукта")
    parser.add_argument("config_file", help="Имя конфигурационного файла JSON")

    args = parser.parse_args()

    with open(args.config_file, "r") as f:
        templates = json.load(f)

    all_versions = []

    for key, template in templates.items():
        generated = generate_versions_from_template(template)
        all_versions.extend(generated)

    all_versions.sort()

    print("Все отсортированные версии:")
    for v in all_versions:
        print(" -", version_to_str(v))

    base_version = parse_version(args.version)

    print("\nВерсии меньше, чем", args.version + ":")
    for v in all_versions:
        if compare_versions(v, base_version):
            print(" <", version_to_str(v))

if __name__ == "__main__":
    main()
