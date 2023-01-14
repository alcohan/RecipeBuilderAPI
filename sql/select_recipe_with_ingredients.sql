SELECT 
    Recipes.Name,
    Recipes.Servings,
    Recipes.PreparationTime,
    SUM(Ingredients.Calories * RecipeIngredients.Quantity) as TotalCalories,
    SUM(Ingredients.Fat * RecipeIngredients.Quantity) as TotalFat,
    SUM(Ingredients.Protein * RecipeIngredients.Quantity) as TotalProtein,
    SUM(Ingredients.Carbohydrates * RecipeIngredients.Quantity) as TotalCarbohydrates,
    SUM(Ingredients.CurrentPrice * RecipeIngredients.Quantity) as TotalPrice,
	COUNT(RecipeIngredients.RecipeIngredientID) as IngredientsQty,
    STUFF((
        SELECT ',' + CAST(RecipeIngredients.IngredientID as varchar) +'|' + CAST(Ingredients.Name as varchar) + '|' + CAST(RecipeIngredients.Quantity as varchar) + '|' + CAST(RecipeIngredients.RecipeIngredientID as varchar)
        FROM 
			RecipeIngredients
			LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
		WHERE
			RecipeIngredients.RecipeID=:placeholder
        FOR XML PATH('')
    ), 1, 1, '') as Ingredients
FROM 
    Recipes
    LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
WHERE 
    Recipes.RecipeID = :placeholder
GROUP BY
    Recipes.Name,
    Recipes.Servings,
    Recipes.PreparationTime