INSERT INTO 
    RecipeIngredients (RecipeID, IngredientID, Quantity)
OUTPUT
    inserted.RecipeIngredientID
VALUES
    (:recipeid, :ingredientid, :qty);