import shlex

from . import core, utils


def run():
    """
    Главная функция - запускает основной цикл программы
    """
    print("***Процесс работы с таблицей***")
    print_help()
    
    while True:
        try:
            user_input = input(">>>Введите команду: ").strip()
            
            if not user_input:
                continue
            
            parts = shlex.split(user_input)
            command = parts[0].lower()
            
            metadata = utils.load_metadata()
            
            if command == "exit":
                print("Выход из программы...")
                break
                
            elif command == "help":
                print("***Процесс работы с таблицей***")
                print_help()
                
            elif command == "create_table":
                if len(parts) < 2:
                    print("Использование: create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...") # noqa: E501
                    continue
                
                table_name = parts[1]
                columns = []
                
                for col_def in parts[2:]:
                    if ":" not in col_def:
                        print(f'Ошибка: Некорректный формат столбца "{col_def}".')
                        break
                    
                    col_name, col_type = col_def.split(":", 1)
                    columns.append((col_name, col_type))
                else:
                    metadata = core.create_table(metadata, table_name, columns)
                    utils.save_metadata(data=metadata)
                
            elif command == "drop_table":
                if len(parts) != 2:
                    print("Использование: drop_table <имя_таблицы>")
                    continue
                
                table_name = parts[1]
                metadata = core.drop_table(metadata, table_name)
                utils.save_metadata(data=metadata)
                
            elif command == "list_tables":
                core.list_tables(metadata)
                
            else:
                print(f'Неизвестная команда: {command}')
                print("Введите 'help' для справки")
                
        except KeyboardInterrupt:
            print("\nПрограмма прервана. Для выхода введите 'exit'")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")