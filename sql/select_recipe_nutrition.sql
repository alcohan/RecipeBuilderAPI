SELECT 
    Recipes.Name,
    Recipes.RecipeID,
    SUM(Ingredients.Calories * RecipeIngredients.Quantity) as TotalCalories,
    SUM(Ingredients.TTLFatGrams * RecipeIngredients.Quantity) as TotalFat,
    SUM(Ingredients.ProteinGrams * RecipeIngredients.Quantity) as TotalProtein,
    SUM(Ingredients.CarbohydratesGrams * RecipeIngredients.Quantity) as TotalCarbohydrates,
    SUM(Ingredients.PortionCost * RecipeIngredients.Quantity) as TotalPrice,
    COUNT(RecipeIngredients.RecipeIngredientID) as IngredientQty
FROM 
    Recipes
    LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
WHERE 
    Recipes.RecipeID = :placeholder
GROUP BY
    Recipes.Name,
    Recipes.RecipeID