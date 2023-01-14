SELECT 
    Recipes.Name,
    Recipes.RecipeID,
    Recipes.Servings,
    Recipes.PreparationTime,
    SUM(Ingredients.Calories * RecipeIngredients.Quantity) as TotalCalories,
    SUM(Ingredients.Fat * RecipeIngredients.Quantity) as TotalFat,
    SUM(Ingredients.Protein * RecipeIngredients.Quantity) as TotalProtein,
    SUM(Ingredients.Carbohydrates * RecipeIngredients.Quantity) as TotalCarbohydrates,
    SUM(Ingredients.CurrentPrice * RecipeIngredients.Quantity) as TotalPrice,
    COUNT(RecipeIngredients.RecipeIngredientID) as IngredientQty
FROM 
    Recipes
    LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
WHERE 
    Recipes.RecipeID = :placeholder
GROUP BY
    Recipes.Name,
    Recipes.Servings,
    Recipes.PreparationTime,
    Recipes.RecipeID