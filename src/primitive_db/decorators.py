import time
from functools import wraps


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок в операциях с базой данных.
    Перехватывает KeyError, ValueError, FileNotFoundError.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: {e}")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except FileNotFoundError as e:
            print(f"Файл не найден: {e}")
            return None
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return None
    return wrapper

def confirm_action(action_name):
    """
    Фабрика декораторов для запроса подтверждения действий.
    
    Args:
        action_name (str): Название действия для вывода в запросе подтверждения
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower() # noqa: E501
            if response == 'y':
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                if len(args) > 0:
                    return args[0]  
                return False
        return wrapper
    return decorator

def log_time(func):
    """
    Декоратор для замера времени выполнения функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд")
        return result
    return wrapper

def create_cacher():
    """
    Функция для создания замыкания с кэшем.
    
    Returns:
        function: Функция cache_result для кэширования результатов
    """
    cache = {}
    
    def cache_result(key, value_func):
        """
        Кэширует результаты выполнения функции.
        
        Args:
            key (hashable): Ключ для кэша
            value_func (callable): Функция для получения значения
            
        Returns:
            Результат выполнения value_func (из кэша или новый)
        """
        if key in cache:
            return cache[key]
        
        result = value_func()
        cache[key] = result
        return result
    
    def clear_cache():
        """Очищает кэш"""
        cache.clear()
    
    cache_result.clear = clear_cache
    
    return cache_result