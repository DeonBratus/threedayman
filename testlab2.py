import json
import os
from tdprint_app.config import addr_config_path  # Убедитесь, что путь корректен

# Пример данных
cluster_name = "cluster1"
printer_name = "kobra"
printer_addr = "192.381.12.48:8741"

# Проверяем, существует ли файл конфигурации
if not os.path.exists(addr_config_path):
    # Если файл не существует, создаем пустой JSON-файл
    with open(addr_config_path, 'w') as file:
        json.dump({}, file)

# Загружаем существующий JSON из файла
with open(addr_config_path, 'r') as file:
    try:
        clusters = json.load(file)
    except json.JSONDecodeError:
        clusters = {}  # Если файл поврежден или пуст, создаем пустой словарь

# Проверяем, существует ли кластер, если нет — создаем
if cluster_name not in clusters:
    clusters[cluster_name] = {}

# Добавляем или обновляем принтер в указанном кластере
clusters[cluster_name][printer_name] = printer_addr

# Сохраняем изменения обратно в файл
with open(addr_config_path, 'w') as file:
    json.dump(clusters, file, indent=4)

print(f"Принтер '{printer_name}' с адресом '{printer_addr}' добавлен или обновлен в кластере '{cluster_name}'.")
