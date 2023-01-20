from db import engine
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from dbutils import to_json, get_table, execute_query, execute_query_with_placeholder

routes = Blueprint('routes', __name__)

@routes.route('/ingredients',methods=['GET', 'POST'])
def get_ingredients():
    if request.method == 'GET':
        return to_json(execute_query("select_all_ingredients"))
    if request.method == 'POST':
        conn = engine.connect()
        with open (f'sql/create_ingredient.sql','r') as file:
            template = text(file.read())
        conn.execute(template, {'placeholder':"NEW"})
        return jsonify({"message":"Created a new Ingredient"}), 200

@routes.route('/pricehistory',methods=['GET'])
def get_price_history():
    return to_json(get_table("PriceHistory"))

@routes.route('/recipes',methods=['GET'])
def get_templates():
    return to_json(execute_query_with_placeholder("select_all_recipes", (0)))

@routes.route('/recipes/templates',methods=['GET'])
def get_recipes():
    return to_json(execute_query_with_placeholder("select_all_recipes", (1)))

@routes.route('/recipes/<recipe_id>/templates')
def get_all_template_by_recipe(recipe_id):
    return to_json(execute_query_with_placeholder("select_all_template_nutrition", (recipe_id)))

@routes.route('/recipes/templates/<template_id>/categorymods', methods=['GET'])
def get_categorymods(template_id):
    return to_json(execute_query_with_placeholder("select_category_weights",(template_id)))

@routes.route('/recipes/templates/<template_id>/categorymods', methods=['PUT'])
def update_categorymods(template_id):
    data = request.get_json()
    conn = engine.connect()
    with open (f'sql/delete_category_weights.sql','r') as file:
        deletetemplate = text(file.read())
    with open (f'sql/upsert_category_weights.sql','r') as file:
        upserttemplate = text(file.read())
    with conn.begin():
        for cat in data:
            cat['categoryid'] = cat['id']
            cat['recipeid'] = template_id
            if float(cat['multiplier']) == 1:
                conn.execute(deletetemplate, cat)
            else:
                conn.execute(upserttemplate,cat)
    return jsonify({"message": "Data updated successfully!"}),200

@routes.route('/recipeingredients',methods=['GET'])
def get_recipe_ingredients():
    return to_json(get_table("RecipeIngredients"))

@routes.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe_info(recipe_id):
    return to_json(execute_query_with_placeholder('select_one_recipe', (recipe_id) ))

@routes.route('/recipes/<recipe_id>/ingredients', methods=['GET', 'POST'])
def get_recipe_quantities(recipe_id):
    if request.method =='GET':
        return to_json(execute_query_with_placeholder('select_recipe_quantities', (recipe_id) ))
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

@routes.route('/recipes/<recipe_id>/ingredients/<ingredient_id>/<recipe_ingredient_id>', methods=['DELETE'])
def delete_recipe_ingredient(recipe_id, ingredient_id, recipe_ingredient_id):
    conn = engine.connect()
    with open (f'sql/delete_recipe_ingredient.sql','r') as file:
        template = text(file.read())
    conn.execute(template, {'id':recipe_ingredient_id})

    return jsonify({"message":"Successfully Deleted."}), 200

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