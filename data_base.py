from pyairtable import Api
from pyairtable.formulas import match

class Bd:
    """Класс для работы с базой данных Airtable"""
    def __init__(self, token, base_id):
        self.base_id = base_id
        self.api = Api(token)
    
    def create_record(self, table_name: str, record: dict) -> dict:
        """Создание записи в БД"""
        table = self.api.table(self.base_id, table_name)
        return table.create(record)
    
    def get_record(self, table_name: str, filter: dict) -> list:
        """Получение записей из БД"""
        formula = match(filter)
        table = self.api.table(self.base_id, table_name)
        return table.all(formula=formula)
    
    def update_record(self, table_name: str, filter: dict, update: dict) -> dict:
        """Обновление записи в БД"""
        formula = match(filter)
        table = self.api.table(self.base_id, table_name)
        records = table.all(formula=formula)
        if len(records) > 0:
            record_id = records[0]['id']
            return table.update(record_id, update)
        return {}