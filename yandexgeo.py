import requests
import time
from datetime import datetime, timedelta
import statistics

URL = "https://yandex.com/time/sync.json?geo=213"

def fetch_response():
    response = requests.get(URL)
    response.raise_for_status()
    return response.text, response.json()

def parse_time_and_zone(json_data):
    server_timestamp_ms = json_data["time"]
    server_time_utc = datetime.utcfromtimestamp(server_timestamp_ms / 1000)
    moscow_data = json_data["clocks"]["213"]
    offset_seconds = moscow_data["offset"]
    offset_hours = offset_seconds // 3600000 if offset_seconds > 100000 else offset_seconds // 3600
    timezone_str = moscow_data["offsetString"]
    local_time = server_time_utc + timedelta(milliseconds=offset_seconds)
    return local_time.strftime("%Y-%m-%d %H:%M:%S"), timezone_str, server_timestamp_ms / 1000

def measure_time_difference():
    t_local_before = time.time()  
    _, json_data = fetch_response()
    _, _, t_server = parse_time_and_zone(json_data)
    delta = abs(t_server - t_local_before)
    return delta, json_data

def main():
    print("=== Сырой ответ от сервера ===")
    raw_text, json_data = fetch_response()
    print(raw_text)

    print("\n=== Человекочитаемое время и временная зона ===")
    human_time, timezone, _ = parse_time_and_zone(json_data)
    print(f"Локальное время: {human_time}")
    print(f"Временная зона: {timezone}")

    print("\n=== Дельты времени (серия из 5 запросов) ===")
    deltas = []
    for i in range(5):
        delta, _ = measure_time_difference()
        deltas.append(delta)
        print(f"{i + 1}) Δt = {delta:.3f} сек")
        time.sleep(0.5)

    avg_delta = statistics.mean(deltas)
    print(f"\nСредняя дельта: {avg_delta:.3f} сек")

if __name__ == "__main__":
    main()
