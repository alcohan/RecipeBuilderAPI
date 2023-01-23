SELECT 
    Recipes.Name,
    Recipes.RecipeID,
    COALESCE(SUM(Ingredients.PortionCost * RecipeIngredients.Quantity),0) as Price,
    COALESCE(SUM(Ingredients.Calories * RecipeIngredients.Quantity),0) as Calories,
    COALESCE(SUM(Ingredients.TTLFatGrams * RecipeIngredients.Quantity),0) as TTLFat,
    COALESCE(SUM(Ingredients.SatFatGrams * RecipeIngredients.Quantity),0) as SatFat,
    COALESCE(SUM(Ingredients.CholesterolMiligrams * RecipeIngredients.Quantity),0) as Cholesterol,
    COALESCE(SUM(Ingredients.SodiumMiligrams * RecipeIngredients.Quantity),0) as Sodium,
    COALESCE(SUM(Ingredients.CarbohydratesGrams * RecipeIngredients.Quantity),0) as Carbohydrates,
    COALESCE(SUM(Ingredients.FiberGrams * RecipeIngredients.Quantity),0) as Fiber,
    COALESCE(SUM(Ingredients.SugarGrams * RecipeIngredients.Quantity),0) as Sugar,
    COALESCE(SUM(Ingredients.ProteinGrams * RecipeIngredients.Quantity),0) as Protein,
    CONVERT(float,COALESCE(SUM(RecipeIngredients.Quantity),0)) as IngredientQty
FROM 
    Recipes
    LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
	LEFT JOIN Categories ON Ingredients.CategoryID = Categories.CategoryID
WHERE 
    Recipes.RecipeID = :placeholder
GROUP BY
    Recipes.Name,
    Recipes.RecipeID