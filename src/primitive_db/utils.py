import json

from constants import DATA_DIR, DEFAULT_ENCODING, JSON_INDENT, METADATA_FILE


def load_metadata(filepath=METADATA_FILE):
    """
    Загружает данные из JSON-файла.
    
    Args:
        filepath (Path или str): Путь к JSON-файлу
    
    Returns:
        dict: Загруженные данные или пустой словарь
    """
    try:
        with open(filepath, 'r', encoding=DEFAULT_ENCODING) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {filepath} поврежден или имеет неверный формат")
        return {}

def save_metadata(data=None, filepath=METADATA_FILE):
    """
    Сохраняет данные в JSON-файл.
    
    Args:
        data (dict): Данные для сохранения
        filepath (Path или str): Путь к JSON-файлу
    """
    if data is None:
        data = {}
    
    try:
        with open(filepath, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(data, f, indent=JSON_INDENT, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}")

def load_table_data(table_name):
    """
    Загружает данные таблицы из JSON-файла.
    
    Args:
        table_name (str): Имя таблицы
    
    Returns:
        list: Данные таблицы или пустой список
    """
    filepath = DATA_DIR / f"{table_name}.json"
    
    try:
        with open(filepath, 'r', encoding=DEFAULT_ENCODING) as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Возвращаем пустой список, если файла нет
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {filepath} поврежден или имеет неверный формат")
        return []

def save_table_data(table_name, data):
    """
    Сохраняет данные таблицы в JSON-файл.
    
    Args:
        table_name (str): Имя таблицы
        data (list): Данные для сохранения
    """
    if not isinstance(data, list):
        print(f"Ошибка: Данные для таблицы {table_name} должны быть списком")
        return
    
    filepath = DATA_DIR / f"{table_name}.json"
    
    try:
        with open(filepath, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(data, f, indent=JSON_INDENT, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}")