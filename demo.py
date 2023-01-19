from flask import Blueprint, render_template
from dbutils import execute_query_with_placeholder

demo = Blueprint('demo',__name__)

@demo.route('/test',methods=["GET"])
def hello():
    return render_template('main.html')

@demo.route('/test/templates')
def templates_page():
    return render_template('view_templates.html')

@demo.route('/test/templates/<template_id>')
def template_page(template_id):
    result=execute_query_with_placeholder('select_one_recipe', (template_id) )[0][0]
    dicts = {}
    for key in result.keys():
        # quantity gets passed as a string for some reason
            
        if key=='IngredientQty':
            dicts[key] = round(float(result[key]),0)
        else:
            if type(result[key]) == float:
                if key=='Price':
                    dicts[key] = round(result[key],2)
                else:
                    dicts[key] = round(result[key],1)
            else:
                dicts[key] = result[key]

    return render_template('edit_template.html',params=dicts)

@demo.route('/test/recipes/<recipe_id>')
def recipe_page(recipe_id):
    result=execute_query_with_placeholder('select_one_recipe', (recipe_id) )[0][0]
    print(result)
    dicts = {}
    for key in result.keys():
        if key=='IngredientQty':
            dicts[key] = round(float(result[key]),0)
        else:
            if type(result[key]) == float:
                if key=='Price':
                    dicts[key] = round(result[key],2)
                else:
                    dicts[key] = round(result[key],1)
            else:
                dicts[key] = result[key]

    return render_template('recipe.html',params=dicts)

@demo.route('/test/ingredients')
def showIngredients():
    return render_template('ingredients.html')

@demo.route('/test/ingredients/<ingredient_id>',methods=["GET"])
def updatePage(ingredient_id):
    result = execute_query_with_placeholder('select_ingredient', (ingredient_id))[0][0]
    dicts = {}
    for key in result.keys():
        if key=='PortionCost':
            dicts[key] = round(result[key]*100,2)
        else:
            dicts[key] = result[key]
    
    return render_template('sample_update.html', params=dicts)