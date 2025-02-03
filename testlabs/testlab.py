import requests

# URL API принтера
api_url = "http://192.168.31.180:7126/printer/objects/query"

# Параметры запроса для получения данных (можно уточнить объекты в документации API)
data = {
    "objects": {
        "print_stats": None,
        "heater_bed": None,
        "extruder": None,
    }
}

# Отправка запроса
try:
    response = requests.post(url=api_url, json=data)
    response.raise_for_status()  # Проверяем успешность запроса
    printer_status = response.json()

    # Обработка и вывод информации
    print("Статус печати:", printer_status['result']['status']['print_stats']['state'])
    print("Температура стола:", printer_status['result']['status']['heater_bed']['temperature'], "°C")
    print("Целевая температура стола:", printer_status['result']['status']['heater_bed']['target'], "°C")
    print("Температура экструдера:", printer_status['result']['status']['extruder']['temperature'], "°C")
    print("Целевая температура экструдера:", printer_status['result']['status']['extruder']['target'], "°C")

except requests.exceptions.RequestException as e:
    print("Ошибка при запросе к API принтера:", e)
