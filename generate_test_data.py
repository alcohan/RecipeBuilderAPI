import random
import datetime
import pyodbc

server = 'tcp:192.168.7.122,1433'
database = 'TestDB' 
username = 'SA' 
password = '4QPR^8s3L%Vx' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
# cnx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cnx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:192.168.7.122,1433;DATABASE=TestDB;UID=SA;PWD=4QPR^8s3L%Vx')

# Create a cursor
cursor = cnx.cursor()

# Generate sample data for Ingredients table
ingredient_names = ['flour', 'sugar', 'eggs', 'milk', 'butter']
ingredient_units = ['g', 'g', 'unit', 'ml', 'g']
for i in range(len(ingredient_names)):
    cursor.execute(f"""
    INSERT INTO Ingredients (Name, Unit, Calories, Fat, Protein, Carbohydrates, CurrentPrice)
    VALUES ('{ingredient_names[i]}', '{ingredient_units[i]}', {random.randint(100, 500)}, {random.randint(10, 50)}, {random.randint(10, 50)}, {random.randint(20, 100)}, {random.randint(1, 10)});
    """)
print("Sample data generated successfully for Ingredients table")

# Generate sample data for PriceHistory table
for i in range(len(ingredient_names)):
    for j in range(3):
        cursor.execute(f"""
        INSERT INTO PriceHistory (IngredientID, Price, Date)
        VALUES ({i+1}, {random.randint(1, 10)}, '{datetime.datetime.now().strftime('%Y-%m-%d')}');
        """)
print("Sample data generated successfully for PriceHistory table")

# Generate sample data for Recipes table
recipe_names = ['pizza', 'cake', 'omlette']
for i in range(len(recipe_names)):
    cursor.execute(f"""
    INSERT INTO Recipes (Name, Servings, PreparationTime)
    VALUES ('{recipe_names[i]}', {random.randint(1, 10)}, {random.randint(15, 60)});
    """)
print("Sample data generated successfully for Recipes table")

# Generate sample data for RecipeIngredients table
for i in range(len(recipe_names)):
    for j in range(2):
        cursor.execute(f"""
        INSERT INTO RecipeIngredients (RecipeID, IngredientID, Quantity)
        VALUES ({i+1}, {j+1}, {random.randint(50, 200)});
        """)
print("Sample data generated successfully for RecipeIngredients table")

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
