import shlex


def parse_where_clause(where_str):
    """
    Парсит условие WHERE.
    
    Args:
        where_str (str): Строка условия, например "age = 28"
    
    Returns:
        dict: Словарь с условием вида {'age': 28}
    """
    if not where_str:
        return None
    
    where_str = where_str.strip()
    
    if '=' in where_str:
        parts = where_str.split('=', 1)
        column = parts[0].strip()
        value = parts[1].strip()
        
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif value.isdigit():
            value = int(value)
        elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
            value = float(value)
        
        return {column: value}
    
    return None

def parse_set_clause(set_str):
    """
    Парсит условие SET.
    
    Args:
        set_str (str): Строка условия, например "age = 29, name = 'John'"
    
    Returns:
        dict: Словарь с обновлениями вида {'age': 29, 'name': 'John'}
    """
    if not set_str:
        return {}
    
    result = {}

    assignments = [a.strip() for a in set_str.split(',')]
    
    for assignment in assignments:
        if '=' in assignment:
            parts = assignment.split('=', 1)
            column = parts[0].strip()
            value = parts[1].strip()
            
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                value = float(value)
            
            result[column] = value
    
    return result

def parse_values(values_str):
    """
    Парсит значения для INSERT.
    
    Args:
        values_str (str): Строка со значениями, например '("Sergei", 28, true)'
    
    Returns:
        list: Список значений
    """
    if not values_str:
        return []
    
    values_str = values_str.strip()
    if values_str.startswith('(') and values_str.endswith(')'):
        values_str = values_str[1:-1]
    
    parts = shlex.split(values_str.replace(',', ' '))
    
    values = []
    for part in parts:
        if part.lower() == 'true':
            values.append(True)
        elif part.lower() == 'false':
            values.append(False)
        elif part.isdigit():
            values.append(int(part))
        elif part.replace('.', '', 1).isdigit() and part.count('.') == 1:
            values.append(float(part))
        else:
            if (part.startswith('"') and part.endswith('"')) or \
               (part.startswith("'") and part.endswith("'")):
                part = part[1:-1]
            values.append(part)
    
    return values