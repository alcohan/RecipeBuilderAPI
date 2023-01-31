SELECT 
    Ingredients.Name
	,RecipeIngredients.RecipeIngredientID
    ,Ingredients.IngredientID
	,CAST(RecipeIngredients.Quantity as float) as Quantity
    ,Categories.Name as Category
FROM 
    RecipeIngredients
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
    LEFT JOIN Categories ON Ingredients.CategoryID = Categories.CategoryID
WHERE 
    RecipeIngredients.RecipeID = :placeholder
ORDER BY
    Categories.CategoryID