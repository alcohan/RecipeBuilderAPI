from app import app
from flask import render_template
from dbutils import execute_query_with_placeholder

@app.route('/test',methods=["GET"])
def hello():
    return render_template('test.html')

@app.route('/test/recipes/<recipe_id>')
def recipe_page(recipe_id):
    result=execute_query_with_placeholder('select_recipe_nutrition', (recipe_id) )[0]
    return render_template('recipe.html',value=result[0])

@app.route('/test/ingredients/<ingredient_id>',methods=["GET"])
def updatePage(ingredient_id):
    result = execute_query_with_placeholder('select_ingredient', (ingredient_id))[0]
    return render_template('sample_update.html', value=result[0])