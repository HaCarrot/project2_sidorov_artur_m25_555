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
            print(f'Ошибка: Некорректный тип данных "{col_type}" для столбца "{col_name}"') # noqa: E501
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