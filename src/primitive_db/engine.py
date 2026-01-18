import shlex
from . import utils
from . import core
from . import parser

def run():
    """
    Главная функция - запускает основной цикл программы
    """
    print_help()
    
    while True:
        try:
            user_input = input(">>> Введите команду: ").strip()
            
            if not user_input:
                continue
            
            parts = shlex.split(user_input)
            command = parts[0].lower()
            
            metadata = utils.load_metadata()
            
            if command == "exit":
                print("Выход из программы...")
                break
                
            elif command == "help":
                print_help()
                
            elif command == "create_table":
                if len(parts) < 2:
                    print("Использование: create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...")
                    continue
                
                table_name = parts[1]
                columns = []
                
                for col_def in parts[2:]:
                    if ":" not in col_def:
                        print(f'Ошибка: Некорректный формат столбца "{col_def}". Используйте имя:тип')
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
                
            elif command == "info":
                if len(parts) != 2:
                    print("Использование: info <имя_таблицы>")
                    continue
                
                table_name = parts[1]
                core.info_table(metadata, table_name)
                
            elif command == "insert":
                if len(parts) < 6 or parts[1].lower() != "into" or parts[3].lower() != "values":
                    print('Использование: insert into <имя_таблицы> values (<значение1>, <значение2>, ...)')
                    continue
                
                table_name = parts[2]
                values_str = " ".join(parts[4:])
                values = parser.parse_values(values_str)
                
                if values:
                    core.insert(metadata, table_name, values)
                
            elif command == "select":
                if len(parts) < 3 or parts[1].lower() != "from":
                    print("Использование: select from <имя_таблицы> [where <условие>]")
                    continue
                
                table_name = parts[2]
                
                if len(parts) > 4 and parts[3].lower() == "where":
                    where_str = " ".join(parts[4:])
                    where_clause = parser.parse_where_clause(where_str)
                    core.select(metadata, table_name, where_clause)
                else:
                    core.select(metadata, table_name)
                
            elif command == "update":
                if len(parts) < 7 or parts[2].lower() != "set" or parts[6].lower() != "where":
                    print('Использование: update <имя_таблицы> set <столбец> = <значение> where <столбец_условия> = <значение_условия>')
                    continue
                
                table_name = parts[1]
                
                set_idx = parts.index("set")
                where_idx = parts.index("where")
                
                set_str = " ".join(parts[set_idx+1:where_idx])
                where_str = " ".join(parts[where_idx+1:])
                
                set_clause = parser.parse_set_clause(set_str)
                where_clause = parser.parse_where_clause(where_str)
                
                if set_clause and where_clause:
                    core.update(metadata, table_name, set_clause, where_clause)
                
            elif command == "delete":
                if len(parts) < 5 or parts[1].lower() != "from" or parts[3].lower() != "where":
                    print("Использование: delete from <имя_таблицы> where <условие>")
                    continue
                
                table_name = parts[2]
                where_str = " ".join(parts[4:])
                where_clause = parser.parse_where_clause(where_str)
                
                if where_clause:
                    core.delete(metadata, table_name, where_clause)
                
            else:
                print(f'Неизвестная команда: {command}')
                print("Введите 'help' для справки")
                
        except KeyboardInterrupt:
            print("\nПрограмма прервана. Для выхода введите 'exit'")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def print_help():
    """
    Выводит справочную информацию
    """
    help_text = """Функции:
<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.
<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.
<command> select from <имя_таблицы> - прочитать все записи.
<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.
<command> info <имя_таблицы> - вывести информацию о таблице.
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выход из программы
<command> help - справочная информация"""
    print(help_text)