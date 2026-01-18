import json
import os
from prettytable import PrettyTable
from . import utils
from . import parser


def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в метаданных.
    
    Args:
        metadata (dict): Текущие метаданные БД
        table_name (str): Имя новой таблицы
        columns (list): Список столбцов в формате [("имя", "тип"), ...]
    
    Returns:
        dict: Обновленные метаданные
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    
    if not table_name or not isinstance(table_name, str):
        print("Ошибка: Некорректное имя таблицы")
        return metadata
    
    columns_with_id = [("ID", "int")] + columns
    
    valid_types = {"int", "str", "bool"}
    for col_name, col_type in columns_with_id:
        if col_type not in valid_types:
            print(f'Ошибка: Некорректный тип данных "{col_type}" для столбца "{col_name}"')
            print(f"Допустимые типы: {', '.join(valid_types)}")
            return metadata
    
    col_names = [col[0] for col in columns_with_id]
    if len(col_names) != len(set(col_names)):
        print("Ошибка: Найдены дублирующиеся имена столбцов")
        return metadata
    
    table_structure = {
        "columns": [
            {"name": col_name, "type": col_type}
            for col_name, col_type in columns_with_id
        ],
        "rows": []  
    }
    
    metadata[table_name] = table_structure
    utils.save_table_data(table_name, [])  
    
    columns_str = ", ".join([f"{col[0]}:{col[1]}" for col in columns_with_id])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    
    return metadata

def drop_table(metadata, table_name):
    """
    Удаляет таблицу из метаданных.
    
    Args:
        metadata (dict): Текущие метаданные БД
        table_name (str): Имя таблицы для удаления
    
    Returns:
        dict: Обновленные метаданные
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    
    del metadata[table_name]
    data_file = f"data/{table_name}.json"
    if os.path.exists(data_file):
        os.remove(data_file)
    
    print(f'Таблица "{table_name}" успешно удалена.')
    
    return metadata

def list_tables(metadata):
    """
    Выводит список всех таблиц.
    
    Args:
        metadata (dict): Текущие метаданные БД
    """
    if not metadata:
        print("В базе данных нет таблиц")
        return
    
    for table_name in metadata.keys():
        print(f"- {table_name}")

def info_table(metadata, table_name):
    """
    Выводит информацию о таблице.
    
    Args:
        metadata (dict): Текущие метаданные БД
        table_name (str): Имя таблицы
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    
    table_data = utils.load_table_data(table_name)
    columns = metadata[table_name]["columns"]
    
    columns_str = ", ".join([f"{col['name']}:{col['type']}" for col in columns])
    
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_str}")
    print(f"Количество записей: {len(table_data)}")

def insert(metadata, table_name, values):
    """
    Вставляет новую запись в таблицу.
    
    Args:
        metadata (dict): Текущие метаданные БД
        table_name (str): Имя таблицы
        values (list): Значения для вставки
    
    Returns:
        bool: True если успешно, False если ошибка
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False
    
    table_data = utils.load_table_data(table_name)
    columns = metadata[table_name]["columns"]
    
    if len(values) != len(columns) - 1:
        print(f'Ошибка: Ожидается {len(columns)-1} значений, получено {len(values)}')
        print(f'Структура таблицы: {", ".join([col["name"] for col in columns[1:]])}')
        return False
    
    for i, value in enumerate(values):
        col_name = columns[i+1]["name"]
        col_type = columns[i+1]["type"]
        
        if col_type == "int" and not isinstance(value, int):
            print(f'Ошибка: Столбец "{col_name}" ожидает тип int, получено {type(value).__name__}')
            return False
        elif col_type == "str" and not isinstance(value, str):
            print(f'Ошибка: Столбец "{col_name}" ожидает тип str, получено {type(value).__name__}')
            return False
        elif col_type == "bool" and not isinstance(value, bool):
            print(f'Ошибка: Столбец "{col_name}" ожидает тип bool, получено {type(value).__name__}')
            return False
    
    if table_data:
        max_id = max(row.get("ID", 0) for row in table_data)
        new_id = max_id + 1
    else:
        new_id = 1
    
    new_row = {"ID": new_id}
    for i, value in enumerate(values):
        col_name = columns[i+1]["name"]
        new_row[col_name] = value
    
    table_data.append(new_row)
    utils.save_table_data(table_name, table_data)
    
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return True

def select(metadata, table_name, where_clause=None):
    """
    Выбирает записи из таблицы.
    
    Args:
        metadata (dict): Текущие метаданные БД
        table_name (str): Имя таблицы
        where_clause (dict): Условие фильтрации
    
    Returns:
        list: Отфильтрованные записи
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return []
    
    table_data = utils.load_table_data(table_name)
    columns = metadata[table_name]["columns"]
    
    if not table_data:
        print(f'Таблица "{table_name}" пуста.')
        return []
    
    if where_clause:
        filtered_data = []
        for row in table_data:
            match = True
            for key, value in where_clause.items():
                if row.get(key) != value:
                    match = False
                    break
            if match:
                filtered_data.append(row)
    else:
        filtered_data = table_data
    
    if filtered_data:
        table = PrettyTable()
        table.field_names = [col["name"] for col in columns]
        
        for row in filtered_data:
            table_row = []
            for col in columns:
                table_row.append(row.get(col["name"], ""))
            table.add_row(table_row)
        
        print(table)
    else:
        print("Записи не найдены.")
    
    return filtered_data

def update(metadata, table_name, set_clause, where_clause):
    """
    Обновляет записи в таблице.
    
    Args:
        metadata (dict): Текущие метаданные БД
        table_name (str): Имя таблицы
        set_clause (dict): Значения для обновления
        where_clause (dict): Условие фильтрации
    
    Returns:
        bool: True если успешно, False если ошибка
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False
    
    table_data = utils.load_table_data(table_name)
    columns = metadata[table_name]["columns"]
    
    column_names = [col["name"] for col in columns]
    for key in set_clause.keys():
        if key not in column_names:
            print(f'Ошибка: Столбец "{key}" не существует в таблице "{table_name}".')
            return False
    
    column_types = {col["name"]: col["type"] for col in columns}
    for key, value in set_clause.items():
        col_type = column_types[key]
        
        if col_type == "int" and not isinstance(value, int):
            print(f'Ошибка: Столбец "{key}" ожидает тип int, получено {type(value).__name__}')
            return False
        elif col_type == "str" and not isinstance(value, str):
            print(f'Ошибка: Столбец "{key}" ожидает тип str, получено {type(value).__name__}')
            return False
        elif col_type == "bool" and not isinstance(value, bool):
            print(f'Ошибка: Столбец "{key}" ожидает тип bool, получено {type(value).__name__}')
            return False
    
    updated_count = 0
    for row in table_data:
        match = True
        if where_clause:
            for key, value in where_clause.items():
                if row.get(key) != value:
                    match = False
                    break
        
        if match:
            updated_count += 1
            for key, value in set_clause.items():
                row[key] = value
    
    if updated_count > 0:
        utils.save_table_data(table_name, table_data)
        print(f'{updated_count} записей в таблице "{table_name}" успешно обновлено.')
        return True
    else:
        print("Записи для обновления не найдены.")
        return False

def delete(metadata, table_name, where_clause):
    """
    Удаляет записи из таблицы.
    
    Args:
        metadata (dict): Текущие метаданные БД
        table_name (str): Имя таблицы
        where_clause (dict): Условие фильтрации
    
    Returns:
        bool: True если успешно, False если ошибка
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False
    
    table_data = utils.load_table_data(table_name)
    
    if where_clause:
        new_data = []
        deleted_ids = []
        for row in table_data:
            match = True
            for key, value in where_clause.items():
                if row.get(key) != value:
                    match = False
                    break
            
            if match:
                deleted_ids.append(row.get("ID"))
            else:
                new_data.append(row)
    else:
        new_data = []
        deleted_ids = [row.get("ID") for row in table_data]
    
    if deleted_ids:
        utils.save_table_data(table_name, new_data)
        for row_id in deleted_ids:
            print(f'Запись с ID={row_id} успешно удалена из таблицы "{table_name}".')
        return True
    else:
        print("Записи для удаления не найдены.")
        return False