from db import engine
from flask import jsonify
from sqlalchemy import text

def get_table(table_name):
    with engine.connect() as conn:
        result = conn.execute(f"SELECT * FROM {table_name}")
        rows = result.fetchall()
        description = result.keys()
        conn.close()
        return (rows, description)

def to_json(object):
    rows = object[0]
    description=object[1]
    return jsonify([dict(zip([column for column in description], row))
        for row in rows])

def execute_query_with_params(sql_file_name, params):
    #connect to database and retrieve ingredients for the recipe_id
    with open(f'sql/{sql_file_name}.sql', 'r') as file:
        sql = file.read()
    template = text(sql)
    template = template.bindparams(placeholder=params)
    with engine.connect() as conn:
        result = conn.execute(template)
        rows = result.fetchall()
        description = result.keys()
        conn.close()
        return (rows,description)

def execute_query(sql_file_name):
    with open(f'sql/{sql_file_name}.sql', 'r') as file:
        sql = file.read()
    with engine.connect() as conn:
        result = conn.execute(sql)
        rows = result.fetchall()
        description = result.keys()
        conn.close()
        return (rows,description)