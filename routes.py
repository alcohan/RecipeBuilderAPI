from db import engine
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from dbutils import to_json, get_table, execute_query, execute_query_with_placeholder

routes = Blueprint('routes', __name__)

@routes.route('/ingredients',methods=['GET', 'POST'])
def get_ingredients():
    if request.method == 'GET':
        return to_json(execute_query("ingredient/select_all_ingredients"))
    if request.method == 'POST':
        conn = engine.connect()
        with open (f'sql/ingredient/create_ingredient.sql','r') as file:
            template = text(file.read())
        conn.execute(template, {'placeholder':"NEW"})
        return jsonify({"message":"Created a new Ingredient"}), 200

@routes.route('/pricehistory',methods=['GET'])
def get_price_history():
    return to_json(get_table("PriceHistory"))

@routes.route('/recipes',methods=['GET', 'POST'])
def recipes():
    if request.method == 'GET':
        return to_json(execute_query_with_placeholder("recipe/select_all_recipes", (0)))
    if request.method == 'POST':
        data = request.get_json()

        with open (f'sql/recipe/create_recipe.sql','r') as file:
            template = text(file.read())
        engine.connect().execute(template, data)
        return jsonify({'message':"Created a new Recipe!"})

@routes.route('/recipes/templates',methods=['GET'])
def get_recipes():
    return to_json(execute_query_with_placeholder("recipe/select_all_recipes", (1)))

@routes.route('/recipes/<recipe_id>/templates')
def get_all_template_by_recipe(recipe_id):
    return to_json(execute_query_with_placeholder("recipe/select_all_template_nutrition", (recipe_id)))

@routes.route('/recipes/templates/<template_id>/categorymods', methods=['GET'])
def get_categorymods(template_id):
    return to_json(execute_query_with_placeholder("template/select_category_weights",(template_id)))

@routes.route('/recipes/templates/<template_id>/categorymods', methods=['PUT'])
def update_categorymods(template_id):
    data = request.get_json()
    conn = engine.connect()
    with open (f'sql/template/delete_category_weights.sql','r') as file:
        deletetemplate = text(file.read())
    with open (f'sql/template/upsert_category_weights.sql','r') as file:
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
    return to_json(execute_query_with_placeholder('recipe/select_one_recipe', (recipe_id) ))

@routes.route('/recipes/<recipe_id>/ingredients', methods=['GET', 'POST'])
def get_recipe_quantities(recipe_id):
    if request.method =='GET':
        return to_json(execute_query_with_placeholder('recipe/select_recipe_quantities', (recipe_id) ))
    if request.method == "POST":
        # Create a new RecipeIngredient for this recipe_id
        data = request.get_json()
        data['recipeid'] = recipe_id
        conn = engine.connect()
        with open(f'sql/recipe/create_recipe_ingredient.sql','r') as file:
            sql = file.read()
        template = text(sql)
        conn.execute(template,data)
        return jsonify({"message": "Data updated successfully!"}), 200

@routes.route('/recipes/<recipe_id>/ingredients/<ingredient_id>/<recipe_ingredient_id>', methods=['DELETE'])
def delete_recipe_ingredient(recipe_id, ingredient_id, recipe_ingredient_id):
    conn = engine.connect()
    with open (f'sql/recipe/delete_recipe_ingredient.sql','r') as file:
        template = text(file.read())
    conn.execute(template, {'id':recipe_ingredient_id})

    return jsonify({"message":"Successfully Deleted."}), 200

@routes.route('/ingredients/<ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    data = request.get_json()
    data['id'] = ingredient_id

    conn=engine.connect()

    with open(f'sql/ingredient/update_ingredient.sql', 'r') as file:
        sql = file.read()
    template = text(sql)
    conn.execute(template, data)
    conn.close()

    return jsonify({"message": "Data updated successfully!"}), 200

@routes.route('/recipes/<recipe_id>/ingredients/batch', methods=['PUT'])
def update_recipe_ingredient(recipe_id):
    updateList = request.get_json()
    conn = engine.connect()
    with open(f'sql/ingredient/update_recipe_ingredient.sql','r') as file:
        sql = file.read()
    template = text(sql)
    with conn.begin():
        for data in updateList: {
            conn.execute(template,data)
        }
    return jsonify({"message": "Data updated successfully!"}), 200