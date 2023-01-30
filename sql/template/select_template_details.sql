SELECT 
	Recipes.Name as Template
	,Recipes.RecipeID as TemplateID
    ,Ingredients.Name
    ,Ingredients.IngredientID
    ,Ingredients.ImageURL
    ,Categories.Name as Category
    ,Ingredients.CategoryID
	,Ingredients.Calories
    ,Ingredients.CarbohydratesGrams
    ,Ingredients.CholesterolMiligrams
    ,Ingredients.FiberGrams
    ,Ingredients.ProteinGrams
    ,Ingredients.SatFatGrams
    ,Ingredients.SodiumMiligrams
    ,Ingredients.SugarGrams
    ,Ingredients.TTLFatGrams

    ,Ingredients.PortionCost
    ,Ingredients.PortionVolume
    ,Ingredients.PortionSize

	,Ingredients.CaseSize
FROM
	RecipeIngredients
	LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
	LEFT JOIN Categories ON Ingredients.CategoryID = Categories.CategoryID
	LEFT JOIN Recipes ON Recipes.RecipeID = RecipeIngredients.RecipeID
WHERE
	IsTemplate = 1
