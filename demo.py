from flask import Blueprint, render_template
from dbutils import execute_query_with_params

demo = Blueprint('demo',__name__)

@demo.route('/test',methods=["GET"])
def hello():
    return render_template('test.html')

@demo.route('/test/recipes/<recipe_id>')
def recipe_page(recipe_id):
    result=execute_query_with_params('select_recipe_nutrition', (recipe_id) )[0]
    return render_template('recipe.html',value=result[0])

@demo.route('/test/ingredients/<ingredient_id>',methods=["GET"])
def updatePage(ingredient_id):
    result = execute_query_with_params('select_ingredient', (ingredient_id))[0][0]
    return render_template('sample_update.html', value=result, portioncost=round(result.PortionCost*100,2))