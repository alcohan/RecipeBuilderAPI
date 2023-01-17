import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:192.168.7.122,1433'
database = 'TestDB' 
username = 'SA' 
password = '4QPR^8s3L%Vx' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = connection.cursor()
# Create a cursor

# Create Ingredients table
cursor.execute("""
CREATE TABLE Ingredients (
    IngredientID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(255) NOT NULL,
    Unit VARCHAR(255) NOT NULL,
    Calories INT,
    Fat INT,
    Protein INT,
    Carbohydrates INT,
    CurrentPrice DECIMAL(10,2)
);
""")
print("Ingredients table created successfully")

# Create PriceHistory table
cursor.execute("""
CREATE TABLE PriceHistory (
    PriceHistoryID INT PRIMARY KEY IDENTITY(1,1),
    IngredientID INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Date DATE NOT NULL,
    FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID)
);
""")
print("PriceHistory table created successfully")

# Create Recipes table
cursor.execute("""
CREATE TABLE Recipes (
    RecipeID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(255) NOT NULL,
    Servings INT,
    PreparationTime INT
);
""")
print("Recipes table created successfully")

# Create RecipeIngredients table
cursor.execute("""
CREATE TABLE RecipeIngredients (
    RecipeIngredientID INT PRIMARY KEY IDENTITY(1,1),
    RecipeID INT NOT NULL,
    IngredientID INT NOT NULL,
    Quantity DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID),
    FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID)
);
""")
print("RecipeIngredients table created successfully")

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()