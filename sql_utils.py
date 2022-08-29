import re
from typing import Any
import constants
import pyodbc
import json
import web_utils

def clean_string(string:str) -> str:
    string = re.sub(r'<.+?>', '', string)
    string = re.sub('%', 'percent', string)
    string = re.sub(r'\\', 'backward_slash', string)
    string = re.sub('/', 'forward_slash', string)
    string = re.sub('@', '', string)
    string = re.sub('&', '', string)
    string = re.sub(r'\|', '', string)
    string = re.sub(r'\*', '', string)
    string = re.sub(r'\?', 'question_mark', string)
    string = re.sub('"', 'double_quote ', string)
    string = re.sub(r'\'', 'quote', string)
    string = re.sub('#', 'hashtag', string)
    string = re.sub(r'\[', 'bkt_open', string)
    string = re.sub(r'\]', 'bkt_close', string)
    string = re.sub(r'\{', 'brace_open', string)
    string = re.sub(r'\}', 'brace_close', string)
    string = re.sub(r'\:', 'colon', string)
    string = re.sub(r'\;', 'semi_colon', string)
    string = re.sub(r'\-', 'minus_sign', string)
    string = re.sub(r'\+', 'plus_sign', string)
    return string

def parse_string(string:str) -> str:
    try:
        string = re.sub('percent', '%', string)
        string = re.sub('backward_slash', r'\\', string)
        string = re.sub('forward_slash', '/',  string)
        string = re.sub('question_mark', '?', string)
        string = re.sub('double_quote', r'"', string)
        string = re.sub('quote', r"'", string)
        string = re.sub('hashtag', '#', string)
        string = re.sub('bkt_open', r'[', string)
        string = re.sub('bkt_close', r']', string)
        string = re.sub('brace_open', r'{', string)
        string = re.sub('brace_close', r'}', string)
        string = re.sub('semi_colon', ';', string)
        string = re.sub('colon', ':', string)
        string = re.sub('minus_sign', '-', string)
        string = re.sub('plus_sign', '+', string)
        return string
    except TypeError:
        print(string)

def parse_element(value:Any):
    value_type = type(value)
    if value_type == str:
        return int(value) if value.isdigit() else f"'{value}'"
    elif value_type in [int, float]:
        return value
    elif value_type==bool:
        return "'True'" if value else "'False'"
    elif value_type==type(None):
        return "NULL"
    elif value_type in [list, dict]:
        return f"'{clean_string(json.dumps(value))}'"
    else:
        raise ValueError(f'Wrong value {value}, can be [str, int, bool, NoneType]')

def parse_dictionnary(property_dict:dict):
    key_string   = ''
    value_string = f''

    identifier = property_dict['id']

    for base_feature_name in constants.FEATURES_OF_INTEREST:
        print(base_feature_name, parse_element(property_dict[base_feature_name]))
        key_string   += f'{base_feature_name},'
        value_string += f'{parse_element(property_dict[base_feature_name])},'

    for image_feature_name in constants.IMAGES_FEATURES:
            web_utils.download_images(image_feature_name, property_dict[image_feature_name], identifier)

    for extra_feature_name in constants.EXTRA_FEATURES:
        key_string   += f'{extra_feature_name},'
        if extra_feature_name in ['latitude', 'longitude']:
            value_string +=  f"{property_dict['location'][extra_feature_name]},"
        elif extra_feature_name == 'pictures':
            value_string += f"{len(property_dict['images'])},"
        elif extra_feature_name == 'price':
            v_string = re.sub(r'[\W_]+', '', property_dict['prices']['primaryPrice'])
            value_string +=  f"{int(v_string)},"

    return key_string, value_string

def table_exists(table_name:str):
    print('Testing if table exists...')
    return f"""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{table_name}'
        """

def is_in_table(table_name:str, identifier:str):
    print('Testing if table exists...')
    return f"""
        SELECT 1 
        FROM {table_name} 
        WHERE id = '{identifier}'
        """

def table_length(table_name:str):
    print('Getting the table length...')
    return f"""
        SELECT count(*) as No_of_Column 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        """

def add_column(table_name, column_name, column_type):
    query = f"""
        IF NOT EXISTS (SELECT '{column_name}' FROM INFORMATION_SCHEMA.columns WHERE table_name = '{table_name}' and column_name = '{column_name}')
        ALTER TABLE {table_name} 
        ADD {column_name} {column_type}"""
    return query

def drop_table(table_name):
    print(f'Dropping table {table_name}')
    return f"""
        DROP TABLE {table_name} 
        """

def create_table(table_name):
    print(f'Creating table {table_name}')
    return f"""
        CREATE TABLE {table_name} 
        (id int primary key)
        """

def add_row(table_name, property_dict:dict):
    key_string, value_string = parse_dictionnary(property_dict)
    return f"""
        IF NOT EXISTS (SELECT * FROM {table_name} WHERE id = '{property_dict['id']}')
        INSERT INTO {table_name} ({key_string[:-1]})values ({value_string[:-1]})
        """

def remove_row(table_name, row_id):
    print(f'Removing row {row_id} from table {table_name}')
    return f"""
        DELETE FROM {table_name} 
        WHERE id={row_id}
        """

def select_item(table_name, identifier):
    return f"""
        SELECT * FROM {table_name}
        WHERE id='{identifier}'
    """

def select_column(table_name, column_name):
    return f"""
        SELECT {column_name} FROM {table_name}
    """

function_dict = {
    'table_exists':table_exists,
    'table_length':table_length,
    'is_in_table':is_in_table,
    'select_item':select_item,
    'select_column':select_column,
    'create_table':create_table,
    'add_column':add_column,
    'add_row':add_row,
    'drop_table':drop_table,
    'remove_row':remove_row
}

def query_table(cursor: pyodbc.Cursor, query_type:str,  query_name:str, *args):
    try:
        query = function_dict[query_name](*args)
    except KeyError:
        print(f'Query name {query_name} does not exist')
        return None
    print(query)
    cursor.execute(query)
    if query_type == 'test':
        result = cursor.fetchall()
        print(f'Querying {args[0]} for query_name {query_name} returned {result}')
        return result
    elif query_type == 'modify':
        cursor.commit()
    print(f'Query {query_name} \n executed')
    
if __name__ == '__main__':
    print('')