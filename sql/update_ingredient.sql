UPDATE 
    Ingredients 
SET 
    Name = :name, 
    Unit = :unit,
    Calories = :calories,
    Fat = :fat,
    Protein = :protein,
    Carbohydrates = :carbs,
    CurrentPrice = :price
WHERE 
    IngredientID = :id