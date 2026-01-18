import json


def load_metadata(filepath="db_meta.json"):
    """
    Загружает данные из JSON-файла.
    
    Args:
        filepath (str): Путь к JSON-файлу
    
    Returns:
        dict: Загруженные данные или пустой словарь
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {filepath} поврежден или имеет неверный формат")
        return {}

def save_metadata(filepath="db_meta.json", data=None):
    """
    Сохраняет данные в JSON-файл.
    
    Args:
        filepath (str): Путь к JSON-файлу
        data (dict): Данные для сохранения
    """
    if data is None:
        data = {}
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}")