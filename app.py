from flask import Flask, jsonify, request, render_template
from os import environ
from flask_cors import CORS

# import pyodbc
from sqlalchemy import create_engine, text

app = Flask(__name__)
CORS(app)

server = environ['SERVER']
database = environ['DATABASE']
username = environ['USERNAME']
password = environ['PASSWORD']

DATABASE_URI = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(DATABASE_URI, pool_size=5,max_overflow=2,pool_timeout=30,pool_recycle=3600)


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

@app.route('/ingredients',methods=['GET'])
def get_ingredients():
    return to_json(get_table("Ingredients"))

@app.route('/pricehistory',methods=['GET'])
def get_price_history():
    return to_json(get_table("PriceHistory"))

@app.route('/recipes',methods=['GET'])
def get_recipes():
    return to_json(execute_query("select_all_recipes"))

@app.route('/recipeingredients',methods=['GET'])
def get_recipe_ingredients():
    return to_json(get_table("RecipeIngredients"))

@app.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe_info(recipe_id):
    return to_json(execute_query_with_params('select_recipe_nutrition', (recipe_id) ))

@app.route('/recipes/<recipe_id>/ingredients', methods=['GET', 'POST'])
def get_recipe_quantities(recipe_id):
    if request.method =='GET':
        return to_json(execute_query_with_params('select_recipe_quantities', (recipe_id) ))
    if request.method == "POST":
        # Create a new RecipeIngredient for this recipe_id
        data = request.get_json()
        data['recipeid'] = recipe_id
        conn = engine.connect()
        with open(f'sql/create_recipe_ingredient.sql','r') as file:
            sql = file.read()
        template = text(sql)
        conn.execute(template,data)
        return jsonify({"message": "Data updated successfully!"}), 200

@app.route('/ingredients/<ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    data = request.get_json()
    data['id'] = ingredient_id

    conn=engine.connect()

    with open(f'sql/update_ingredient.sql', 'r') as file:
        sql = file.read()
    template = text(sql)
    conn.execute(template, data)
    conn.close()

    return jsonify({"message": "Data updated successfully!"}), 200

@app.route('/recipes/<recipe_id>/ingredients/batch', methods=['PUT'])
def update_recipe_ingredient(recipe_id):
    updateList = request.get_json()
    conn = engine.connect()
    with open(f'sql/update_recipe_ingredient.sql','r') as file:
        sql = file.read()
    template = text(sql)
    with conn.begin():
        for data in updateList: {
            conn.execute(template,data)
        }
    return jsonify({"message": "Data updated successfully!"}), 200

# Test routes DELETEME
@app.route('/test',methods=["GET"])
def hello():
    return render_template('test.html')

@app.route('/test/recipes/<recipe_id>')
def recipe_page(recipe_id):
    result=execute_query_with_params('select_recipe_nutrition', (recipe_id) )[0]
    return render_template('recipe.html',value=result[0])

@app.route('/test/ingredients/<ingredient_id>',methods=["GET"])
def updatePage(ingredient_id):
    result = execute_query_with_params('select_ingredient', (ingredient_id))[0]
    return render_template('sample_update.html', value=result[0])

if __name__ == "__main__":
    app.run()