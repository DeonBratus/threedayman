import json
from config import addr_config_path
import os
class TdPrinterService:
    def __init__(self):
        self.addr_filename = addr_config_path

    def add_printer(self, name: str, addr: str, clustername: str):
        if self.__check_is_exist():
            clusters = self.__get_data()
            msg = self.__write_data(clustername, addr, name, clusters)
            return msg
        
    def get_printers(self):
        if self.__check_is_exist():
            data = self.__get_data()
            return data

    def __check_is_exist(self):
        if not os.path.exists(addr_config_path):
            with open(addr_config_path, 'w') as file:
                json.dump({}, file)
        return True
    

    def __get_data(self):
        # Загружаем существующий JSON из файла
        with open(addr_config_path, 'r') as file:
            try:
                clusters = json.load(file)
            except json.JSONDecodeError:
                clusters = {}
        return clusters


    def __write_data(self, cluster_name: str, printer_name: str, printer_addr:str, clusters):
        # Проверяем, существует ли кластер, если нет — создаем
        if cluster_name not in clusters:
            clusters[cluster_name] = {}

        # Добавляем или обновляем принтер в указанном кластере
        clusters[cluster_name][printer_name] = printer_addr

        # Сохраняем изменения обратно в файл
        with open(addr_config_path, 'w') as file:
            json.dump(clusters, file, indent=4)
        return {"msg": "Принтер '{printer_name}' с адресом '{printer_addr}' добавлен или обновлен в кластере '{cluster_name}'."}
