from db import engine
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from dbutils import to_json, get_table, execute_query, execute_query_with_params

routes = Blueprint('routes', __name__)

@routes.route('/ingredients',methods=['GET'])
def get_ingredients():
    return to_json(get_table("Ingredients"))

@routes.route('/pricehistory',methods=['GET'])
def get_price_history():
    return to_json(get_table("PriceHistory"))

@routes.route('/recipes',methods=['GET'])
def get_recipes():
    return to_json(execute_query("select_all_recipes"))

@routes.route('/recipeingredients',methods=['GET'])
def get_recipe_ingredients():
    return to_json(get_table("RecipeIngredients"))

@routes.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe_info(recipe_id):
    return to_json(execute_query_with_params('select_recipe_nutrition', (recipe_id) ))

@routes.route('/recipes/<recipe_id>/ingredients', methods=['GET', 'POST'])
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

@routes.route('/ingredients/<ingredient_id>', methods=['PUT'])
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

@routes.route('/recipes/<recipe_id>/ingredients/batch', methods=['PUT'])
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