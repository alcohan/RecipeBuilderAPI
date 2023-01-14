SELECT 
    Ingredients.Name,
	RecipeIngredients.RecipeIngredientID,
    Ingredients.IngredientID,
	RecipeIngredients.Quantity
FROM 
    RecipeIngredients
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
WHERE 
    RecipeIngredients.RecipeID = :placeholder